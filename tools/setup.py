import subprocess
import os
import platform
from tools.colors import Colors
import threading


class SceSetupTool:
    """
    This class handles checking installation of the proper tools
    as well as checking if the proper directories are cloned for
    sce development
    """
    operating = ""
    color = Colors()
    rpc = threading.Semaphore(value=0)
    core = threading.Semaphore(value=0)
    discord = threading.Semaphore(value=0)

    def check_installation(self, name, command, link):
        """
        This method is called to check if the proper software is installed
        if the software is installed the console will print out a message and move on
        if not then the console will redirect the user to the site to install the softare
            Parameters:
            name (string): name of the software to check for
            command (string): the name of the command that the command line wiill execute
            link (string): link to the site to install the software
        """
        devnull = open(os.devnull, 'wb')
        subprocess.check_call(command, stdout=devnull, stderr=subprocess.STDOUT, shell=True)
        try:
            self.color.print_yellow(name + " found", True)
        except subprocess.CalledProcessError:
            self.color.print_red(name + " not found", True)
            print("visit here to install: ")
            self.color.print_purple(link, True)
            print("press enter to continue: ")
            choice = input()
            while choice != "":
                choice = input()

    def check_os(self):
        """
        This method checks the user's os and stores it into a class variable
        """
        self.operating = platform.system()
        self.color.print_purple(self.operating, True)

    def check_directory(self, name):
        """
        This method checks for a given directory
        if the directory is found then git reset is called if work is not found
        if the directory does not exist then clone the directory
            Parameters:
            name (string): the name of the directory
        """
        if os.path.isdir(name):
            self.color.print_pink(name + " directory found", True)
        else:
            self.color.print_red(name + " directory not found, cloning for you", True)
            devnull = open(os.devnull, 'wb')
            subprocess.check_call("git clone https://github.com/SCE-Development/" + name,
                                  stdout=devnull, stderr=subprocess.STDOUT, shell=True)
            #subprocess.check_call(name + "/npm install", stdout=devnull, stderr=subprocess.STDOUT,
                                  #shell=True)
            if name == "Core-v4":
                os.system("echo test")

    def check_docker(self):
        """
        This method is used to check for docker software
        """
        self.check_installation("docker", "docker --version", "https://docs.docker.com/desktop/")

    def check_mongo(self):
        """
        This method checks for mongo installation
        """
        self.check_installation("mongo", "mongo --version",
                                "https://www.mongodb.com/try/download/community")

    def setup_rpc(self):
        """
        This method is used to specifically check for the sce-rpc directory
        """
        devnull = open(os.devnull, 'wb')
        if os.path.isdir("sce-rpc"):
            self.color.print_pink("sce-rpc directory found", True)
            subprocess.check_call("git -C sce-rpc checkout master", stdout=devnull, stderr=subprocess.STDOUT,
                                  shell=True)
            subprocess.check_call("git -C sce-rpc fetch origin", stdout=devnull, stderr=subprocess.STDOUT,
                                  shell=True)
            subprocess.check_call("git -C sce-rpc reset --hard origin/master",
                                  stdout=devnull, stderr=subprocess.STDOUT, shell=True)
        else:
            subprocess.check_call("git clone https://github.com/SCE-Development/sce-rpc",
                                  stdout=devnull, stderr=subprocess.STDOUT, shell=True)
            '''
            if self.operating == "Windows":
                os.system("sce-rpc/setup.bat")
            else:
                os.system("sce-rpc/setup.sh")
            '''
        self.rpc.release()

    def setup_core_v4(self):
        """
        This method checks for the corev4 directory
        """
        self.check_directory("Core-v4")
        self.core.release()

    def setup_discord_bot(self):
        """
        This method checks for the discord bot directory
        """
        self.check_directory("SCE-discord-bot")
        self.discord.release()

    def print_status(self):
        dict_directories = {
            'rpc': False,
            'core': False,
            'discord': False
        }

        print("waiting for rpc...")
        print("waiting for core...")
        print("waiting for discord...\n")
        print(" =========================== ")
        print("|                           |")

        while 1:
            if self.rpc.acquire(blocking=False):
                dict_directories['rpc'] = True
                print("| rpc finished              |")
            if self.core.acquire(blocking=False):
                dict_directories['core'] = True
                print("| core finished             |")
            if self.discord.acquire(blocking=False):
                dict_directories['discord'] = True
                print("| discord finished          |")
            if all(value for value in dict_directories.values()):
                print("|                           |")
                print("| setup complete            |")
                print("|                           |")
                print(" =========================== ")
                exit(0)

    def handle_setup(self):
        t1 = threading.Thread(target=self.setup_rpc)
        t2 = threading.Thread(target=self.setup_core_v4)
        t3 = threading.Thread(target=self.setup_discord_bot)
        t4 = threading.Thread(target=self.print_status)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
