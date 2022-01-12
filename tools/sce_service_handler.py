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
        sce_path = os.environ.get('SCE_PATH')
        if not sce_path:
            self.colors.print_red('Error: current working path not registered, please re-run the setup script.')
            return

        db_path = os.path.join(sce_path, 'mongo', 'data', 'db')
            
        # Test if docker is installed or not running
        try:
            subprocess.check_output('docker ps', stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            # On Windows: Installed but not running
            # If need detailed error msg:
            # output = err.output.decode()
            # self.colors.print_red(output)
            self.colors.print_red('To run MongoDB, ensure your Docker Desktop is running.')
            return
        except FileNotFoundError:
            # On Windows: not installed
            # On Mac or Linux: installed but not running OR not installed
            if self.user_os == "Windows":
                self.colors.print_red('To run MongoDB, please install Docker Desktop! If you already have, you may need to reload this terminal.')
                return
            # Test for Mac or Linux
            try:
                subprocess.check_call(
                    'docker -v',
                    stdout=devnull,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                self.colors.print_red('To run MongoDB, ensure your Docker Desktop is running.')
                return
            except FileNotFoundError:
                # Not installed
                self.colors.print_red('To run MongoDB, please install Docker Desktop! If you already have, you may need to reload this terminal.')
                return

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
