import os
import subprocess


class SceDockerHandler:
    container_dict = {
        'frontend': 'cd Core-v4 && npm run frontend',
        'server': 'cd Core-v4 && npm run server',
        'led-sign': 'cd SCE-RPC/server/led_sign/ && python3 led_sign_server.py',
        '2d-printing': 'cd SCE-RPC/server/printing/ && python3 printing_server.py',
        '3d-printing': 'cd SCE-RPC/server/printing_3d/ && python3 print_3d_server.py',
        'main_endpoints': 'cd Core-v4/api && npm run main_endpoints',
        'logging': 'cd Core-v4/api && npm run logging',
        'google_api': 'cd Core-v4/api && npm run google_api',
        'discord-bot': True,
        'sce-rpc': True,
        'core-v4': True,
        'mongo': True,
    }

    def __init__(self, services):
        self.services = services

    def run_services(self):
        if not self.services:
            self.all_systems_go()
        else:
            for service in self.services:
                if service == 'print':
                    self.print_usage()
                elif service not in self.container_dict:
                    print(
                        f"{service} does not exist. If you would like to see the list of available services type: run -s print")
                elif service == "sce-rpc":
                    self.run_sce_rpc()
                elif service == 'core-v4':
                    self.run_core_v4()
                elif service == 'discord-bot':
                    self.run_discord_bot()
                elif service == 'mongo':
                    self.run_mongodb()
                else:
                    subprocess.run(self.container_dict[service])

    def print_usage(self):
        print('Available Services (case sensitive):')
        for key in self.container_dict:
            print('\t', key)

    def run_mongodb(self):
        if os.path.exists('~/data/db'):
            subprocess.run('mongod --dbpath ~/data/db')
        else:
            subprocess.run('mongod')

    def run_core_v4(self):
        # self.run_mongodb()
        subprocess.Popen(self.container_dict['frontend'], shell=True)
        subprocess.Popen(self.container_dict['server'], shell=True)

    def run_sce_rpc(self):

        subprocess.Popen('python3 led_sign_server.py',
                         cwd='SCE-RPC/server/led_sign/',
                         shell=True)
        # subprocess.Popen(self.container_dict['3d-printing'], shell=True)
        # subprocess.Popen(self.container_dict['2d-printing'], shell=True)
        subprocess.Popen('npm start', cwd='SCE-RPC', shell=True)

    def run_discord_bot(self):
        subprocess.Popen('npm start', cwd='SCE-discord-bot/', shell=True)

    def all_systems_go(self):
        self.run_sce_rpc()
        self.run_core_v4()
        self.run_discord_bot()
