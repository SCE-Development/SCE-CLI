import os
import subprocess
import platform
from tools.colors import Colors


class SceServiceHandler:
    colors = Colors()

    def __init__(self, services):
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
        devnull = open(os.devnull, 'wb')
        try:
            subprocess.check_output('docker ps', stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            output = err.output.decode()
            self.colors.print_red(output)
            self.colors.print_red('To run MongoDB, ensure your Docker Desktop is running.')
            return
        except FileNotFoundError as err:
            try:
                subprocess.check_call(
                    'docker -v',
                    stdout=devnull,
                    stderr=subprocess.STDOUT, shell=True
                )    
            except subprocess.CalledProcessError:
                self.colors.print_red('To run MongoDB, ensure your Docker Desktop is running.')
                return

            self.colors.print_red(
                'To run MongoDB, please install Docker Desktop! If you already have, you may need to reload this terminal.'
            )
            return

        sce_path = os.environ.get('SCE_PATH')

        if not sce_path:
            self.colors.print_red('Error: current working path not registered, please re-run the setup script.')
            return

        db_path = os.path.join(sce_path, 'mongo', 'data', 'db')
        subprocess.Popen(
            f'''docker run -it -p 27017:27017 -v {db_path}:/data/db mongo''',
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
