import argparse
from tools.setup import SceSetupTool
from tools.sce_proto_generator import SceProtoGenerator
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
args = parser.parse_args()

if args.command == 'setup':
    setup = SceSetupTool()
    setup.setup()
elif args.command == 'presubmit':
    test_project = ScePresubmitHandler(args.project)
    test_project.handle_testing()
elif args.command == 'generate':
    generator = SceProtoGenerator(args.proto[0], args.language)
    generator.handle_proto_generation()
elif args.command == 'test':
    setup = SceSetupTool()
    setup.add_sce_alias()
