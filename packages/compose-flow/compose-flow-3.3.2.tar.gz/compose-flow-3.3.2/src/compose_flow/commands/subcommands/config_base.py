import os
import shlex
import sys
import tempfile

from compose_flow import docker, shell

from .base import BaseSubcommand


class ConfigBaseSubcommand(BaseSubcommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # put this on hold for now.  in order to get this working on jenkins agents that
        # are not swarm managers.  this test should probably occur somewhere closer to when
        # a config is being pulled out of a local docker instance
        # self._check_swarm()

        # the original values for config items whose values have been rendered
        # for example, the value for `FOO=runtime://` will be whatever $FOO is at runtime
        # similarly, the value for `FOO=runtime://BAR` will be whatever $BAR is at runtime
        self._rendered_config = {}

    def _check_swarm(self):
        """
        Checks to see if Docker is setup as a swarm
        """
        try:
            self.execute('docker config ls')
        except shell.ErrorReturnCode_1 as exc:
            message = exc.stderr.decode('utf8').strip().lower()

            if 'this node is not a swarm manager' in message:
                self.init_swarm(prompt=True)
            else:
                raise

    def edit(self) -> None:
        with tempfile.NamedTemporaryFile('w') as fh:
            path = fh.name

            self.render_buf(fh, runtime_config=False)

            fh.flush()

            editor = os.environ.get('EDITOR', os.environ.get('VISUAL', 'vi'))

            self.execute(f'{editor} {path}', _fg=True)

            self.push(path)

    def init_swarm(self, prompt: bool = False) -> None:
        """
        Prompts to initialize a local swarm
        """
        try:
            self.execute('docker config ls')
        except:
            pass
        else:
            return

        environment = self.workflow.environment

        docker_host = environment.data.get('DOCKER_HOST')
        if docker_host:
            docker_host_message = f'docker host at {docker_host}'
        else:
            docker_host_message = 'docker host'

        message = (
            f'It looks like your {docker_host_message} is not setup for a swarm.'
            '\nSwarm is needed in order to store configuration directly on Docker itself.'
            '\n\nWould you like to configure it now? [N|y]: '
        )

        init_swarm = True
        if prompt:
            print(message, end='')
            response = sys.stdin.readline().strip()

            response = response.upper() or 'N'
            if response != 'Y':
                init_swarm = False

        if init_swarm:
            self.execute('docker swarm init')

    def push(self, path: str = None) -> None:
        """
        Saves an environment into the swarm
        """
        args = self.workflow.args

        path = path or args.path
        if not path:
            return self.print_subcommand_help(__doc__, error='path needed to load')

        docker.load_config(args.config_name, path)

    def render_buf(self, buf, data: dict = None, runtime_config: bool = True):
        data = data or self.data  # pylint: disable=E1101

        # reset runtime variables
        if not runtime_config:
            data.update(self._rendered_config)

        lines = []
        for k, v in data.items():
            lines.append(f'{k}={v}')

        buf.write('\n'.join(sorted(lines)))
