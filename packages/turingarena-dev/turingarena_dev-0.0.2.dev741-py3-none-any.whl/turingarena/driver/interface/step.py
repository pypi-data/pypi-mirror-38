from abc import abstractmethod
from collections import namedtuple

from turingarena.driver.interface.execution import Assignments
from turingarena.driver.interface.phase import ExecutionPhase
from turingarena.driver.interface.nodes import IntermediateNode, Bindings
from turingarena.driver.interface.variables import ReferenceDirection

class StepExecutor:
    @abstractmethod
    def execute(self, bindings: Bindings, step: 'Step') -> Assignments:
        pass


class Step(IntermediateNode, namedtuple("Step", ["children"])):
    __slots__ = []

    def _driver_run(self, context):
        assert self.children

        if context.phase is not None:
            return self._run_children(context)
        else:
            result = context.result()
            for phase in ExecutionPhase:
                if phase == ExecutionPhase.UPWARD and self._get_direction() != ReferenceDirection.UPWARD:
                    continue
                result = result.merge(self._run_children(context.extend(result)._replace(
                    phase=phase,
                )))

            return result

    def _run_children(self, context):
        result = context.result()
        for n in self.children:
            result = result.merge(n.driver_run(context.extend(result)))
        return result

    def _get_declaration_directions(self):
        for n in self.children:
            yield from n.declaration_directions

    def _get_direction(self):
        if not self.declaration_directions:
            return None
        [direction] = self.declaration_directions
        return direction

    def _get_reference_actions(self):
        for n in self.children:
            yield from n.reference_actions

    def _describe_node(self):
        if self._get_direction() is None:
            direction = "no direction"
        else:
            direction = self._get_direction().name.lower()
        yield f"step {direction} "
        for n in self.children:
            yield from self._indent_all(n.node_description)
