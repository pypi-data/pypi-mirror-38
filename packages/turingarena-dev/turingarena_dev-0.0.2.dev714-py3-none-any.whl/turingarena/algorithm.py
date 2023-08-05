import logging
import os
from collections import namedtuple
from contextlib import contextmanager, ExitStack

from turingarena import InterfaceExit, TimeLimitExceeded, AlgorithmError
from turingarena.driver.client import DriverProcessClient, SandboxClient
from turingarena.driver.engine import DriverClientEngine
from turingarena.driver.proxy import MethodProxy

logger = logging.getLogger(__name__)


class Algorithm(namedtuple("Algorithm", [
    "source_path", "language_name", "interface_path",
])):
    @contextmanager
    def run(self, time_limit=None):
        with ExitStack() as stack:
            sandbox_dir = os.environ["TURINGARENA_SANDBOX_DIR"]

            sandbox_client = SandboxClient(sandbox_dir)
            sandbox_process_dir = stack.enter_context(sandbox_client.run(
                source_path=self.source_path,
                language_name=self.language_name,
                interface_path=self.interface_path,
            ))

            driver_process_client = DriverProcessClient(sandbox_process_dir)

            with driver_process_client.connect() as connection:
                algorithm_process = AlgorithmProcess(connection)
                with algorithm_process.run(time_limit=time_limit):
                    try:
                        yield algorithm_process
                    except InterfaceExit:
                        pass
                algorithm_process.exit()


class AlgorithmSection:
    def __init__(self, engine):
        self.info_before = None
        self.info_after = None
        self._engine = engine

    @contextmanager
    def _run(self, *, time_limit):
        self.info_before = self._engine.get_info()
        yield self
        self.info_after = self._engine.get_info()

        if time_limit is not None and self.time_usage > time_limit:
            raise TimeLimitExceeded(
                self,
                f"Time limit exceeded: {self.time_usage} {time_limit}",
                self.info_after,
            )

    @property
    def time_usage(self):
        return self.info_after.time_usage - self.info_before.time_usage


class AlgorithmProcess(AlgorithmSection):
    def __init__(self, connection):
        super().__init__(engine=DriverClientEngine(self, connection))

        self.procedures = MethodProxy(self._engine, has_return_value=False)
        self.functions = MethodProxy(self._engine, has_return_value=True)
        self.terminated = False

    def section(self, *, time_limit=None):
        section_info = AlgorithmSection(self._engine)
        return section_info._run(time_limit=time_limit)

    def checkpoint(self):
        self._engine.send_checkpoint()

    def exit(self):
        self._engine.send_exit()

    def fail(self, message, exc_type=AlgorithmError):
        if self.terminated:
            info = None
        else:
            info = self._engine.get_info(kill=True)
        
        raise exc_type(self, message, info)

    @contextmanager
    def run(self, **kwargs):
        assert not self.terminated
        self._engine.get_response_ok() # ready
        with self._run(**kwargs) as section:
            yield section
        self.terminated = True

    def check(self, condition, message, exc_type=AlgorithmError):
        if not condition:
            self.fail(message, exc_type)
