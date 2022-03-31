import argparse
import platform
import os
from tools.setup import SceSetupTool
from tools.sce_service_handler import SceServiceHandler
from tools.sce_presubmit_handler import ScePresubmitHandler

sce_dir = os.environ['SCE_PATH']
parser = argparse.ArgumentParser()
sub_parser = parser.add_subparsers(required=True, dest='command')

setup_parser = sub_parser.add_parser('setup', help='Setup the sce tool')

run_parser = sub_parser.add_parser('run', help='Run an sce service')
run_parser.add_argument(
    'service', nargs='*',
    help='SCE Service name'
)
run_parser.add_argument(
    '--dbpath',
    help='Specify a path for the volume used by MongoDB.'
)

presubmit_parser = sub_parser.add_parser('presubmit', help='Project to run presubmit checks for')
presubmit_parser.add_argument(
    '--project', '-p', nargs='+',
    help='Project to run presubmit checks for.'
)

def directory(path):
    if os.path.isdir(path):
        return path
    else:
        raise ValueError(f'{path}: No such directory')

linker_parser = sub_parser.add_parser('link', help='Link existing sce project clones')
linker_parser.add_argument(
    'project', help='Name of project to link against'
)
linker_parser.add_argument(
    '-p', '--path',
    help='path to project clone (working directory by default)', 
    type=directory, default=os.getcwd()
)

args = parser.parse_args()

# cd into the dev folder if we are in windows.
# we dont need to do it for unix/macos because
# changing the directory is part of the sce alias.
if args.command == 'setup':
    setup = SceSetupTool(sce_dir)
    setup.setup()
else:
    if platform.system() == 'Windows':
        place = os.environ["SCE_PATH"]
        os.chdir(place)
    if args.command == 'presubmit':
        test_project = ScePresubmitHandler(args.project)
        test_project.handle_testing()
    elif args.command == 'run':
        os.chdir(sce_dir)
        handler = SceServiceHandler(args.service, args.dbpath)
        handler.run_services()
    elif args.command == 'link':
        os.symlink(os.path.abspath(args.path), os.path.join(sce_dir, args.project))
