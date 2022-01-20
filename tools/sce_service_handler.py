import os
import subprocess
import platform
from tools.colors import Colors
from tools.shared_utils import check_docker_status


class SceServiceHandler:
    colors = Colors()
    mongo_volume_path = None

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
        
        set_mongo_path_res = self.set_mongo_volume_path(dbpath)
        if set_mongo_path_res['error']:
            self.colors.print_red(set_mongo_path_res['message'])
            return

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
                    self.run_mongodb()
                else:
                    subprocess.check_call(self.service_dict[service],
                                          shell=True)

    def print_usage(self):
        print('Available Services (case sensitive):')
        for key in self.service_dict:
            print('\t', key)

    def run_mongodb(self):
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

        subprocess.Popen(
            f'''docker run -p 27017:27017 -v {self.mongo_volume_path}:/data/db mongo''',
            stdin=subprocess.DEVNULL,
            shell=True
        )
        

    def run_core_v4(self):
        self.run_mongodb()
        subprocess.Popen(self.service_dict['frontend'], shell=True)
        subprocess.Popen(self.service_dict['server'], shell=True)

    def run_discord_bot(self):
        subprocess.Popen('cd SCE-discord-bot && npm start', shell=True)

    def all_systems_go(self):
        self.run_core_v4()
        self.run_discord_bot()

    def set_mongo_volume_path(self, path=None):
        sce_path = os.environ.get('SCE_PATH')
        if not sce_path:
            self.colors.print_red(
                
            )
            return {
                'error': True,
                'message': (
                    'Error: Please run the setup command first. ' \
                    'If you already have, you may need to reload your shell.'
                )
            }

        self.mongo_volume_path = os.path.join(sce_path, 'mongo', 'data', 'db')
        if path is None:
            return { 'error': False }

        try:
            os.mkdir(path)
            self.mongo_volume_path = path
            return { 'error': False }
        except FileExistsError:
            self.mongo_volume_path = path
            return { 'error': False }
        except Exception:
            return {
                'error': True,
                'message': (
                    'The path you entered does not appear to be a valid directory.' \
                    'Please check it and try again.'
                )
            }
