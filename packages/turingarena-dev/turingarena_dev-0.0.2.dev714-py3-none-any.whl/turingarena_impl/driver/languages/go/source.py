import logging
import os
import shutil
import subprocess

from turingarena_impl.driver.sandbox.process import PopenProcess
from turingarena_impl.driver.sandbox.rlimits import set_rlimits
from turingarena_impl.driver.source import AlgorithmSource, CompilationFailed

logger = logging.getLogger(__name__)


class GoAlgorithmSource(AlgorithmSource):
    def compile(self, compilation_dir):
        with open(os.path.join(compilation_dir, "skeleton.go"), "w") as f:
            self.language.skeleton_generator().generate_to_file(self.interface, f)

        shutil.copyfile(self.source_path, os.path.join(compilation_dir, "solution.go"))

        cli = [
            "go",
            "build",
            "-o", self.executable_path(compilation_dir),
            os.path.join(compilation_dir, "skeleton.go"),
            os.path.join(compilation_dir, "solution.go"),
        ]
        logger.debug(f"Running {' '.join(cli)}")
        try:
            subprocess.run(
                cli,
                universal_newlines=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            if e.returncode != 0:
                raise CompilationFailed
            raise

    def executable_path(self, compilation_dir):
        return os.path.join(compilation_dir, "algorithm")

    def create_process(self, compilation_dir, connection):
        # sandbox_path = pkg_resources.resource_filename(__name__, "sandbox.py")

        return PopenProcess(
            connection,
            [self.executable_path(compilation_dir)],
            preexec_fn=set_rlimits,
        )
