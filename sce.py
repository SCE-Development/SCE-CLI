import argparse
import platform
import os
from tools.setup import SceSetupTool
from tools.sce_proto_generator import SceProtoGenerator
from tools.sce_service_handler import SceServiceHandler
from tools.sce_presubmit_handler import ScePresubmitHandler

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
args = parser.parse_args()

# cd into the dev folder if we are in windows.
# we dont need to do it for unix/macos because
# changing the directory is part of the sce alias.
if platform.system() == "Windows":
    place = os.environ["SCE_PATH"]
    os.chdir(place)

if args.command == 'setup':
    setup = SceSetupTool()
    setup.setup()
elif args.command == 'presubmit':
    test_project = ScePresubmitHandler(args.project)
    test_project.handle_testing()
elif args.command == 'generate':
    generator = SceProtoGenerator(args.proto[0], args.language)
    generator.handle_proto_generation()
elif args.command == 'run':
    handler = SceServiceHandler(args.service)
    handler.run_services()
elif args.command == 'test':
    setup = SceSetupTool()
    setup.add_sce_alias()
