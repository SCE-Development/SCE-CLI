import argparse
from tools.setup import SceSetupTool
from tools.sce_proto_generator import SceProtoGenerator

parser = argparse.ArgumentParser()

parser.add_argument(
    'command', help='Setup for the SCE tool to run ' +
    '(setup, run, presubmit, etc.)')
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
elif args.command == 'generate':
    generator = SceProtoGenerator(args.proto[0], args.language)
    generator.handle_proto_generation()
