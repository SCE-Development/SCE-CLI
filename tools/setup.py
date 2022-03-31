import subprocess
import os
import platform
from tools.colors import Colors
from tools.utils import check_docker_status, prompt_user, prompt_user_yn

class SceSetupTool:
    """
    This class handles checking installation of the proper tools
    as well as checking if the proper directories are cloned for
    sce development
    """
    operating = ""
    color = Colors()
    devnull = open(os.devnull, 'wb')
    docker_is_running = True

    def __init__(self, sce_path):
        self.operating = platform.system()
        self.sce_path = sce_path

    def check_installation(self, name, command, link):
        """
        This method is called to check if the proper software is
        installed if the software is installed the console will
        print out a message and move on if not then the console
        will redirect the user to the site to install the software
            Parameters:
            name (string): name of the software to check for
            command (string): the name of the command
                that the command line will execute
            link (string): link to the site to install the software
        """
        try:
            subprocess.check_call(command, stdout=self.devnull,
                                  stderr=subprocess.STDOUT, shell=True)
            self.color.print_yellow(name + " found")
        except subprocess.CalledProcessError:
            self.color.print_red(name + " not found")
            print("visit here to install: ")
            self.color.print_purple(link)
            input("press enter to continue: ")
    
    def check_directory(self, name):
        """
        This method checks for a given directory
        if the directory is found then git reset is called if work is not found
        if the directory does not exist then clone the directory
            Parameters:
            name (string): the name of the directory
        """
        if os.path.isdir(name):
            self.color.print_pink(name + " directory found")
        else:
            self.color.print_red(name + ' directory not found')
            clone_yn = prompt_user_yn(f'would you like to clone {name} (y or n)? ')
            if clone_yn == 'y':
                subprocess.check_call("git clone "
                                      + "https://github.com/SCE-Development/"
                                      + name, stderr=subprocess.STDOUT, shell=True)
            else:
                self.color.print_red(f'skipping setup for {name}. If you wish to clone {name}'
                        ' and link it with sce later, run:')
                print(f'    sce clone {name}')
                print(f'    sce link {name}')
                self.color.print_red(f'and run the setup for {name} with: ')
                print(f'    sce setup -p {name}')
                input('Enter to continue: ')

    def check_docker(self):
        """
        This method checks for docker installation and
        if it is running
        """
        docker_status = check_docker_status()
        if not docker_status['is_installed']:
            self.color.print_red('Docker not found')
            print("Follow the instruction to install: ")
            self.color.print_purple('https://docs.docker.com/get-docker/')
            input("Press enter to exit setup: ")
            return
        if not docker_status['is_running']:
            self.docker_is_running = False
        self.color.print_yellow('Docker found')

    
    def check_node(self): 
        """
            This method checks for node installation
        """
        self.check_installation("npm", "npm -v",
                                    "https://nodejs.org/en/download/")

    def write_alias_to_file(self, file_name):
        try:
            subprocess.check_call(
                f'grep -rl \"alias sce=\" {file_name}',
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError:
            with open(file_name, 'a') as file:
                file.write('\n')
                file.write(f"export SCE_PATH={self.sce_path}")
                file.write('\n')
                file.write(f'alias sce="python3 {self.sce_path}/sce.py"')
                file.write('\n')

    def unix_rc_path(self):
        SHELL = os.environ['SHELL'][os.environ['SHELL'].rfind('/')+1:]
        HOME_PATH = os.environ['HOME']
        return f'{HOME_PATH}/.{SHELL}rc'

    def add_alias_unix(self):
        self.write_alias_to_file(self.unix_rc_path())

    def add_alias_windows(self):
        subprocess.check_call("py -m pip install cx_Freeze",
                              stderr=subprocess.STDOUT, shell=True)
        subprocess.check_call("py -m pip install idna",
                              stderr=subprocess.STDOUT, shell=True)
        subprocess.check_call("py setup.py build",
                              stderr=subprocess.STDOUT, shell=True)
        os.chdir("build")
        current_dir = os.getcwd()
        os.chdir("..")
        where_at = os.path.join(current_dir, os.listdir("build")[0])
        current_dir = os.getcwd()
        subprocess.check_call("setx SCE_PATH " + current_dir,
                                stderr=subprocess.STDOUT, shell=True)
        self.color.print_yellow("Hold on, to finish setup put")
        self.color.print_green(where_at)
        self.color.print_yellow("in your Path environment variable.")

    def add_sce_alias(self):
        if self.operating == "Windows":
            self.add_alias_windows()
        elif self.operating == "Linux" or self.operating == "Darwin":
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
        copy_command = "copy" if self.operating == "Windows" else "cp"
        if not os.path.exists("config.json"):
            os.system(f"{copy_command} config.example.json config.json")
        subprocess.check_call("npm install",
                            stderr=subprocess.STDOUT, shell=True)
        os.chdir("..")

    def setup_dev(self):
        """
        This method conditionally creates a config.json file.
        """
        config_example_path = os.path.join("config", "config.example.json")
        config_path = os.path.join("config", "config.json")
        copy_command = "copy" if self.operating == "Windows" else "cp"
        if not os.path.exists(config_example_path):
            os.system(f"{copy_command} {config_example_path} {config_path}")
        if self.operating == "Windows":
            command = "py"
        else:
            command = "python3"
        subprocess.check_call(
            f'{command} -m pip install -r ./requirements.txt --user',
            stderr=subprocess.STDOUT, shell=True)

    def setup(self):
        self.color.print_purple(f'Detected OS: {self.operating}')

        self.check_docker()
        self.check_node()

        self.setup_core_v4()
        self.setup_discord_bot()
        self.setup_dev()

        self.add_sce_alias()
        if self.operating == "Windows":
            self.color.print_yellow("""
The npm install step in the three projects may have created unwanted files.
Open the projects and delete any unfamiliar untracked files.
                                    """)

        if not self.docker_is_running:
            self.color.print_pink(
                '''\
Please start Docker Desktop before running backend services.
                '''
            )
