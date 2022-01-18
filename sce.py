import argparse
import platform
import os
import sys
from tools.setup import SceSetupTool
from tools.sce_service_handler import SceServiceHandler
from tools.sce_presubmit_handler import ScePresubmitHandler

def set_mongo_path(handler, path):
    set_mongo_path_res = handler.set_mongo_volume_path(path)
    if set_mongo_path_res['error']:
        handler.colors.print_red(set_mongo_path_res['message'])
        sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument(
    'command', help='Setup for the SCE tool to run ' +
    '(setup, run, presubmit, etc.)')
parser.add_argument(
    '--project', '-p', nargs='+', help='Project to run presubmit checks for.')
parser.add_argument(
    '--proto', nargs=1,
    help='The language(s) to generate proto code.')
parser.add_argument(
    '--language', nargs='+',
    help='The language(s) to generate proto code.')
parser.add_argument(
    '--service', '-s', nargs='*',
    help='SCE Service name')
parser.add_argument(
    '--dbpath',
    help='Specify a custom path for the volume used by MongoDB.'
)
args = parser.parse_args()

# cd into the dev folder if we are in windows.
# we dont need to do it for unix/macos because
# changing the directory is part of the sce alias.
if args.command == 'setup':
    setup = SceSetupTool()
    setup.setup()
else:
    if platform.system() == 'Windows':
        place = os.environ["SCE_PATH"]
        os.chdir(place)
    if args.command == 'presubmit':
        test_project = ScePresubmitHandler(args.project)
        test_project.handle_testing()
    elif args.command == 'run':
        handler = SceServiceHandler(args.service)
        if args.dbpath:
            set_mongo_path(handler, args.dbpath)
        handler.run_services()
    elif args.command == 'test':
        setup = SceSetupTool()
        setup.add_sce_alias()
