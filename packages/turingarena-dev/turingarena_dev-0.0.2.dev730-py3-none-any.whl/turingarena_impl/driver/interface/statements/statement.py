from abc import abstractmethod
from typing import List

from bidict import bidict

from turingarena_impl.driver.interface.common import ImperativeStructure, AbstractSyntaxNodeWrapper
from turingarena_impl.driver.interface.nodes import IntermediateNode
from turingarena_impl.driver.interface.variables import ReferenceStatus


class AbstractStatement(ImperativeStructure):
    __slots__ = []

    def validate(self):
        return []

    @property
    def needs_flush(self):
        return False

    @property
    def variables_to_declare(self):
        return frozenset(self._get_variables_to_declare())

    def _get_variables_to_declare(self):
        for inst in self.intermediate_nodes:
            for a in inst.reference_actions:
                if a.reference.index_count == 0 and a.status == ReferenceStatus.DECLARED:
                    yield a.reference.variable

    @property
    def variables_to_allocate(self):
        return list(self._get_allocations())

    def _get_allocations(self):
        return []

    @property
    def intermediate_nodes(self) -> List[IntermediateNode]:
        return list(self._get_intermediate_nodes())

    @abstractmethod
    def _get_intermediate_nodes(self):
        pass

    @property
    def comment(self):
        return self._get_comment()

    def _get_comment(self):
        return None

    @property
    def does_break(self):
        return False


class Statement(AbstractStatement, AbstractSyntaxNodeWrapper):
    __slots__ = []

    @staticmethod
    def get_statement_classes():
        from .call import CallStatement
        from turingarena_impl.driver.interface.statements.callback import ReturnStatement
        from .loop import LoopStatement, BreakStatement
        from .for_loop import ForStatement
        from .if_else import IfStatement
        from turingarena_impl.driver.interface.statements.callback import ExitStatement
        from .switch import SwitchStatement
        from .io import CheckpointStatement, ReadStatement, WriteStatement

        return bidict({
            "checkpoint": CheckpointStatement,
            "read": ReadStatement,
            "write": WriteStatement,
            "call": CallStatement,
            "return": ReturnStatement,
            "exit": ExitStatement,
            "for": ForStatement,
            "if": IfStatement,
            "loop": LoopStatement,
            "break": BreakStatement,
            "switch": SwitchStatement,
        })

    @staticmethod
    def compile(ast, context):
        return Statement.get_statement_classes()[ast.statement_type](ast=ast, context=context)

    @property
    def statement_type(self):
        return self.ast.statement_type

    def __str__(self):
        from turingarena_impl.driver.generator import StatementDescriptionCodeGen
        return "".join(StatementDescriptionCodeGen().statement(self))


class SyntheticStatement(AbstractStatement):
    __slots__ = ["statement_type", "_comment", "__dict__"]

    def __init__(self, statement_type, comment, **kwargs):
        self.statement_type = statement_type
        self._comment = comment
        self.__dict__ = kwargs

    def _get_intermediate_nodes(self):
        return []

    def _get_comment(self):
        return f"({self._comment})"
