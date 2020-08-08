import os
import subprocess
import platform


class SceServiceHandler:
    def __init__(self, services):
        self.user_os = platform.system()
        self.py_command = "py" if self.user_os == "Windows" else "python3"
        self.services = services
        self.service_dict = {
            'frontend': 'cd Core-v4 && npm start',
            'server': 'cd Core-v4 && npm run server',
            'led-sign': f'cd SCE-RPC/server/led_sign/ && \
                {self.py_command} led_sign_server.py',
            '2d-printing': f'cd SCE-RPC/server/printing/ && \
                {self.py_command} printing_server.py',
            '3d-printing': f'cd SCE-RPC/server/printing_3d/ && \
                {self.py_command} print_3d_server.py',
            'discord': True,
            'sce-rpc': True,
            'core-v4': True,
            'mongo': True,
        }

    def run_services(self):
        if not self.services:
            print('damn')
            self.all_systems_go()
        else:
            for service in self.services:
                if service == 'print':
                    self.print_usage()
                elif service not in self.service_dict:
                    print(
                        f"{service} does not exist. Avaliable services are:",
                        [item for item in list(self.service_dict.keys())])
                elif service == "sce-rpc":
                    self.run_sce_rpc()
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
        if os.path.exists('~/data/db'):
            subprocess.Popen('mongod --dbpath ~/data/db')
        else:
            subprocess.Popen('mongod')

    def run_core_v4(self):
        self.run_mongodb()
        subprocess.Popen(self.service_dict['frontend'], shell=True)
        subprocess.Popen(self.service_dict['server'], shell=True)

    def run_sce_rpc(self):
        subprocess.Popen(self.service_dict['led-sign'], shell=True)
        subprocess.Popen(self.service_dict['3d-printing'], shell=True)
        subprocess.Popen(self.service_dict['2d-printing'], shell=True)
        subprocess.Popen('npm start', cwd='SCE-RPC', shell=True)

    def run_discord_bot(self):
        subprocess.Popen('cd SCE-discord-bot && npm start', shell=True)

    def all_systems_go(self):
        self.run_sce_rpc()
        self.run_core_v4()
        self.run_discord_bot()
