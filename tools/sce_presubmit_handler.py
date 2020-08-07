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
        'sce-rpc': {
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

    def __init__(self, project):
        print(project)
        self.project = project
        """
        this is a constructor, send in args.project from sce.py here.
        """

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

    def project_tests(self):
        if self.project != 'dev':
            os.chdir(self.project)
        project_tests = self.test_commands[self.project]
        for test_name in project_tests.keys():
            self.run_test(test_name, project_tests[test_name])
        if self.project != 'dev':
            os.chdir('..')
