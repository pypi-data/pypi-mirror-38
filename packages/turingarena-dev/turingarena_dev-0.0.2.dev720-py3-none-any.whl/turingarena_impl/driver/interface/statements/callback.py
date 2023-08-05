import logging

from collections import namedtuple

from turingarena.driver.exceptions import InterfaceError
from turingarena_impl.driver.interface.block import Block, BlockNode
from turingarena_impl.driver.interface.callables import CallbackPrototype
from turingarena_impl.driver.interface.execution import RequestSignature
from turingarena_impl.driver.interface.phase import ExecutionPhase
from turingarena_impl.driver.interface.expressions import Expression, SyntheticExpression
from turingarena_impl.driver.interface.nodes import IntermediateNode, StatementIntermediateNode, RequestLookaheadNode
from turingarena_impl.driver.interface.statements.statement import Statement, SyntheticStatement
from turingarena_impl.driver.interface.variables import ReferenceAction, ReferenceStatus, ReferenceDirection
from turingarena_impl.driver.interface.execution import ProcessExplicitlyKilled

logger = logging.getLogger(__name__)


class CallbackImplementation(IntermediateNode, CallbackPrototype):
    __slots__ = []

    @property
    def synthetic_body(self):
        return SyntheticCallbackBody(self)

    @property
    def body(self):
        inner_context = self.context.local_context.with_reference_actions(
            ReferenceAction(reference=p.as_reference(), status=ReferenceStatus.DECLARED)
            for p in self.parameters
        )
        return Block(
            ast=self.ast.body if self.ast.body else self.default_body,
            context=inner_context,
        )

    @property
    def default_body(self):
        fake_ast_body = [
            namedtuple("write", ["statement_type", "arguments"])("write", [
                namedtuple("expression", ["expression_type", "variable_name", "indices"])("reference_subscript", p.name, "")
                for p in self.parameters
            ])
        ]
        if self.has_return_value:
            return_var = namedtuple("expression", ["expression_type", "variable_name", "indices"])("reference_subscript", "_result", "")
            fake_ast_body += [
                namedtuple("read", ["statement_type", "arguments"])("read", [return_var]),
                namedtuple("ret", ["statement_type", "value"])("return", return_var),
            ]
        return namedtuple("body", ["statements"])(fake_ast_body)

    def validate(self):
        yield from self.prototype.validate()

    def _generate_inner_nodes(self):
        yield CallbackCallNode(self)
        yield from self.body.flat_inner_nodes
        if not self.has_return_value:
            yield RequestLookaheadNode()
            yield CallbackReturnNode(callback=self, return_statement=None)

    @property
    def body_node(self):
        return BlockNode.from_nodes(self._generate_inner_nodes())

    def _driver_run(self, context):
        assert context.phase is None
        context.send_driver_upward(1)  # has callbacks
        context.send_driver_upward(self.context.callback_index)
        self.body_node.driver_run(context)

    def _get_declaration_directions(self):
        return self.body_node.declaration_directions


class SyntheticCallbackBody(namedtuple("SyntheticCallbackBody", ["implementation"])):
    @property
    def synthetic_statements(self):
        callback_index = self.implementation.context.callback_index
        yield SyntheticStatement("write", "requesting a callback", arguments=[
            SyntheticExpression("int_literal", value=1),
        ])
        comment = f"index of this callback: {callback_index} = {self.implementation.name}"
        yield SyntheticStatement("write", comment, arguments=[
            SyntheticExpression("int_literal", value=callback_index),
        ])
        yield from self.implementation.body.synthetic_statements


class CallbackCallNode(StatementIntermediateNode):
    def _get_reference_actions(self):
        for p in self.statement.parameters:
            yield ReferenceAction(reference=p.reference, status=ReferenceStatus.DECLARED)

    def _get_declaration_directions(self):
        yield ReferenceDirection.UPWARD

    def _driver_run(self, context):
        if context.phase is ExecutionPhase.REQUEST:
            for p in self.statement.parameters:
                r = p.as_reference()
                value = context.bindings[r]
                context.send_driver_upward(value)

    def _describe_node(self):
        yield "callback_call"


class CallbackReturnNode(IntermediateNode, namedtuple("CallbackReturnNode", [
    "callback",
    "return_statement",
])):
    def _driver_run(self, context):
        if context.phase is ExecutionPhase.REQUEST:
            request = context.request_lookahead
            command = request.command
            if not command == "callback_return":
                raise InterfaceError(f"expecting 'callback_return', got '{command}'")

            return context.result()._replace(assignments=list(self._get_assignments(context)))

    def _get_assignments(self, context):
        has_return_value = bool(int(context.receive_driver_downward()))
        if self.return_statement is not None:
            if not has_return_value:
                raise InterfaceError(
                    f"callback is a function, "
                    f"but the provided implementation did not return anything"
                )
            value = int(context.receive_driver_downward())
            yield self.return_statement.value.reference, value
        else:
            if has_return_value:
                raise InterfaceError(
                    f"callback is a procedure, "
                    f"but the provided implementation returned something"
                )

    def _describe_node(self):
        yield f"callback return {self.return_statement or self.callback.name}"


class ReturnStatement(Statement):
    __slots__ = []

    @property
    def value(self):
        return Expression.compile(self.ast.value, self.context.expression(reference=True))

    def _get_intermediate_nodes(self):
        yield RequestLookaheadNode()
        yield CallbackReturnNode(callback=None, return_statement=self)

    def validate(self):
        yield from self.value.validate()

    def _get_reference_actions(self):
        yield ReferenceAction(reference=self.value.reference, status=ReferenceStatus.RESOLVED)


class ExitStatement(Statement, IntermediateNode):
    __slots__ = []

    def _get_intermediate_nodes(self):
        yield RequestLookaheadNode()
        yield self

    def validate(self):
        # TODO: check that exit is used only in valid places
        return []

    def _get_first_requests(self):
        yield RequestSignature("exit")

    def _get_reference_actions(self):
        return []

    def _driver_run(self, context):
        if context.phase is ExecutionPhase.REQUEST:
            command = context.request_lookahead.command
            if command != "exit":
                raise InterfaceError(f"Expecting exit, got {command}")
            raise ProcessExplicitlyKilled

    @property
    def does_break(self):
        return True
