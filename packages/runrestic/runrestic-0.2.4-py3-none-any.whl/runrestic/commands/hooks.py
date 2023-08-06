import logging
import subprocess

from runrestic.restic import ResticRepository

logger = logging.getLogger(__name__)


def execute_hook(config: dict, name: str, repo: ResticRepository):
    cmd = config.get(name)
    if cmd:
        logger.info(' - executing hook: {cmd}'.format(cmd=cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
            process_rc = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            process_rc = e.returncode

        logger.debug(output)

        if repo.log_metrics:
            repo.log['restic_{name}'.format(name=name)] = {}
            repo.log['restic_{name}'.format(name=name)]['rc'] = process_rc

        logger.info('   ' + ("✓" if process_rc == 0 else "✕"))

        return process_rc

    return 0
