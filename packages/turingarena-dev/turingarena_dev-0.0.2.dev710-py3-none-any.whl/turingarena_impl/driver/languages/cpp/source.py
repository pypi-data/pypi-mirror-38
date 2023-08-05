import logging
import os
import subprocess
from subprocess import CalledProcessError

import pkg_resources

from turingarena_impl.driver.sandbox.process import PopenProcess
from turingarena_impl.driver.sandbox.rlimits import set_rlimits
from turingarena_impl.driver.source import AlgorithmSource, CompilationFailed

logger = logging.getLogger(__name__)


class CppAlgorithmSource(AlgorithmSource):
    __slots__ = []

    def _compile_source(self, compilation_dir):
        cli = [
            "g++", "-c", "-O2", "-std=c++17", "-Wall",
            "-o", self._source_object_path(compilation_dir),
            self.source_path
        ]

        logger.debug("Compiling source: " + " ".join(cli))
        subprocess.run(cli, universal_newlines=True, check=True)

    def _compile_skeleton(self, compilation_dir):
        cli = [
            "g++", "-c", "-O2", "-std=c++17",
            "-o", self._skeleton_object_path(compilation_dir),
            self._skeleton_path(compilation_dir),
        ]

        logger.debug("Compiling skeleton: " + " ".join(cli))
        subprocess.run(cli, universal_newlines=True, check=True)

    def _link_executable(self, compilation_dir):
        cli = [
            "g++", "-static",
            "-o", self.executable_path(compilation_dir),
            self._skeleton_object_path(compilation_dir),
            self._source_object_path(compilation_dir)
        ]

        logger.debug("Linking executable: " + " ".join(cli))
        subprocess.run(cli, universal_newlines=True, check=True)

    def compile(self, compilation_dir):
        with open(self._skeleton_path(compilation_dir), "w") as f:
            self.language.skeleton_generator().generate_to_file(self.interface, f)

        try:
            self._compile_source(compilation_dir)
            self._compile_skeleton(compilation_dir)
            self._link_executable(compilation_dir)
        except CalledProcessError:
            raise CompilationFailed

    @staticmethod
    def executable_path(compilation_dir):
        return os.path.join(compilation_dir, "algorithm")

    @staticmethod
    def _skeleton_path(compilation_dir):
        return os.path.join(compilation_dir, "skeleton.cpp")

    @staticmethod
    def _skeleton_object_path(compilation_dir):
        return os.path.join(compilation_dir, "skeleton.o")

    @staticmethod
    def _source_object_path(compilation_dir):
        return os.path.join(compilation_dir, "source.o")

    def create_process(self, compilation_dir, connection):
        sandbox_path = pkg_resources.resource_filename(__name__, "sandbox.py")

        return PopenProcess(
            connection,
            ["python3", sandbox_path, self.executable_path(compilation_dir)],
            preexec_fn=set_rlimits,
        )
