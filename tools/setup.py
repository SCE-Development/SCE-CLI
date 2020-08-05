import subprocess
import os
import platform
from tools.colors import Colors


class SceSetupTool:
    """
    This class handles checking installation of the proper tools
    as well as checking if the proper directories are cloned for
    sce development
    """
    operating = ""
    color = Colors()
    devnull = open(os.devnull, 'wb')

    def check_installation(self, name, command, link):
        """
        This method is called to check if the proper software is
        installed if the software is installed the console will
        print out a message and move on if not then the console
        will redirect the user to the site to install the softare
            Parameters:
            name (string): name of the software to check for
            command (string): the name of the command
                that the command line will execute
            link (string): link to the site to install the software
        """
        try:
            subprocess.check_call(command, stdout=self.devnull,
                                  stderr=subprocess.STDOUT, shell=True)
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
        self.color.print_purple(f'Detected OS: {self.operating}', True)

    def setup_rpc(self):
        """
        This method is used to specifically check for the sce-rpc directory
        """
        if os.path.isdir("sce-rpc"):
            self.color.print_pink("sce-rpc directory found", True)
        else:
            os.system("git clone https://github.com/SCE-Development/sce-rpc")
        os.chdir("sce-rpc")

        if self.operating == "Windows":
            os.system("setup.bat")
        else:
            os.system("./setup.sh")
        os.chdir("..")

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
            self.color.print_red(
                name + " directory not found, cloning for you", True)
            subprocess.check_call("git clone"
                                  + "https://github.com/SCE-Development/"
                                  + name, stderr=subprocess.STDOUT, shell=True)

    def check_mongo(self):
        """
        This method checks for mongo installation
        """
        self.check_installation("mongo", "mongo --version",
                                "https://www.mongodb.com/"
                                + "try/download/community")

    def write_alias_to_file(self, file_name):
        sce_path = os.getcwd()
        try:
            subprocess.check_call(
                f'grep -rl \"alias sce=\" {file_name}',
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError:
            with open(file_name, 'a') as file:
                file.write('\n')
                file.write(f"SCE_PATH={sce_path}")
                file.write('\n')
                file.write(f'alias sce="python3 {sce_path}/sce.py"')
                file.write('\n')

    def add_alias_unix(self):
        HOME_PATH = os.environ["HOME"]
        BASHRC_PATH = f'{HOME_PATH}/.bashrc'
        if self.operating == "Darwin":
            ZSHRC_PATH = f"{HOME_PATH}/.zshrc"
            if os.path.isfile(BASHRC_PATH):
                self.write_alias_to_file(BASHRC_PATH)
                self.write_alias_to_file('dookie')
            if os.path.isfile(ZSHRC_PATH):
                self.write_alias_to_file(ZSHRC_PATH)
        elif self.operating == "Linux":
            BASH_PROFILE_PATH = f"{HOME_PATH}/.bash_profile"
            if os.path.isfile(BASHRC_PATH):
                self.write_alias_to_file(BASHRC_PATH)
            elif os.path.isfile(BASH_PROFILE_PATH):
                self.write_alias_to_file(BASH_PROFILE_PATH)

    def add_alias_windows(self):
        subprocess.check_call("pip install cx_Freeze",
                              stderr=subprocess.STDOUT, shell=True)
        subprocess.check_call("pip install idna",
                              stderr=subprocess.STDOUT, shell=True)
        subprocess.check_call("py setup.py build",
                              stderr=subprocess.STDOUT, shell=True)
        where_at = os.path.join(os.getcwd(), os.listdir("build")[0])
        self.color.print_pink(f"""
HOLD UP!!!
To use the sce command line tool, add this to your path:
{where_at}
                              """, True)

    def add_sce_alias(self):
        self.check_os()
        if self.operating == "Windows":
            self.add_alias_windows()
        else:
            self.add_alias_unix()

    def setup_core_v4(self):
        """
        This method checks for the corev4 directory
        """
        self.check_directory("Core-v4")
        os.chdir("Core-v4")
        subprocess.check_call(
            "npm install", stderr=subprocess.STDOUT, shell=True)
        if self.operating == "Windows":
            subprocess.check_call("py setup.py", stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, shell=True)
        else:
            subprocess.check_call("python3 setup.py", stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, shell=True)
        subprocess.check_call("npm run server-install",
                              stderr=subprocess.STDOUT, shell=True)
        os.chdir("..")

    def setup_discord_bot(self):
        """
        This method checks for the discord bot directory
        """
        self.check_directory("SCE-discord-bot")
        os.chdir("SCE-discord-bot")
        subprocess.check_call("npm install",
                              stderr=subprocess.STDOUT, shell=True)
        os.chdir("..")

    def setup(self):
        self.check_os()
        self.check_mongo()

        self.setup_rpc()
        self.setup_core_v4()
        self.setup_discord_bot()

        self.add_sce_alias()
        self.color.print_yellow("""
Make sure you you cd into Core-v4/api
and then ls. After then delete the
folders.
                                """)
