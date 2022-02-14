import os
import sys
import signal
import subprocess
import platform
from tools.colors import Colors
from tools.shared_utils import check_docker_status


class SceServiceHandler:
    colors = Colors()

    def __init__(self, services, dbpath=None):
        self.user_os = platform.system()
        self.py_command = "py" if self.user_os == "Windows" else "python3"
        self.services = services
        self.service_dict = {
            'frontend': 'cd Core-v4 && npm start',
            'server': 'cd Core-v4 && npm run server',
            'discord': True,
            'core-v4': True,
            'mongo': True,
        }
        self.set_mongo_volume_path(dbpath)

    def run_services(self):
        if not self.services:
            self.all_systems_go()
        else:
            for service in self.services:
                if service == 'print':
                    self.print_usage()
                elif service not in self.service_dict:
                    print(
                        f"{service} does not exist. Avaliable services are:",
                        [item for item in list(self.service_dict.keys())])
                elif service == 'core-v4':
                    self.run_core_v4()
                elif service == 'discord':
                    self.run_discord_bot()
                elif service == 'mongo':
                    self.run_mongodb(len(self.services) > 1)
                else:
                    subprocess.Popen(self.service_dict[service],
                                        shell=True)

    def print_usage(self):
        print('Available Services (case sensitive):')
        for key in self.service_dict:
            print('\t', key)

    def run_mongodb(self, detached=False):
        docker_status = check_docker_status()
        if not docker_status['is_installed']:
            self.colors.print_red(
                'To run MongoDB, please install Docker Desktop! '\
                'If you already have, you may need to reload your shell.'
            )
            return

        if not docker_status['is_running']:
            self.colors.print_red('To run MongoDB, ensure your Docker daemon is running.')
            return

        docker_command = f'''docker run -it -p 27017:27017 -d -v {self.mongo_volume_path}:/data/db mongo'''

        subprocess.Popen(
            docker_command,
            stdout=subprocess.PIPE,
            shell=True
        )

    def run_core_v4(self):
        self.run_mongodb(True)
        subprocess.Popen(self.service_dict['frontend'], shell=True)
        subprocess.Popen(self.service_dict['server'], shell=True)

    def run_discord_bot(self):
        subprocess.Popen('cd SCE-discord-bot && npm start', shell=True).communicate()

    def all_systems_go(self):
        self.run_core_v4()
        self.run_discord_bot()

    def set_mongo_volume_path(self, path=None):
        sce_path = os.environ.get('SCE_PATH')
        if not sce_path:
            self.colors.print_red(
                'Error: Please run the setup command first. ' \
                    'If you already have, you may need to reload your shell.'
            )
            sys.exit(1)

        if path is None:
            self.mongo_volume_path = os.path.join(sce_path, 'mongo', 'data', 'db')
        else:
            self.mongo_volume_path = path
