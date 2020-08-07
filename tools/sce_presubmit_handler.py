import subprocess
import os
import platform


class ScePresubmitHandler:
    if platform.system() == "Windows":
        dev_command = "py -m flake8"
    else:
        dev_command = "python3 -m flake8"

    test_commands = {
        'Core-v4': {
            'api-test': 'npm run api-test',
            'lint': 'npm run lint',
            'frontend-test': 'npm run frontend-test',
            'build': 'npm run build'
        },
        'SCE-RPC': {
            'test': 'npm run test',
            'lint': 'npm run lint',
            'flake8': dev_command
        },
        'SCE-discord-bot': {
            'lint': 'npm run lint'
        },
        'dev': {
            'flake8': dev_command
        }
    }

    def __init__(self, projects):
        if projects is None:
            self.projects = list(self.test_commands.keys())
        else:
            self.projects = projects

    def run_test(self, test_name, command):
        num_dots = 37 - len(test_name)
        dots = "." * num_dots
        try:
            subprocess.check_output(command, shell=True)
            dots_passed = dots + "passed"
            print('     ' + test_name + dots_passed)
        except subprocess.CalledProcessError:
            dots_failed = dots + "failed"
            print('     ' + test_name + dots_failed)

    def print_usage(self):
        print(f"""
        Please enter a valid project.
        Valid projects are: {list(self.test_commands.keys())}.
        """)

    def test_project(self, project):
        project_valid = project in self.test_commands
        if not project or not project_valid:
            self.print_usage()
            return
        print('\nRunning tests for: ' + project)
        if platform.system() == "Windows":
            place = os.environ["SCE_PATH"]
            os.chdir(place)
        if project != 'dev':
            os.chdir(project)
        project_tests = self.test_commands[project]
        for test_name in project_tests.keys():
            self.run_test(test_name, project_tests[test_name])
        if project != 'dev':
            os.chdir('..')

    def handle_testing(self):
        for project in self.projects:
            self.test_project(project)
