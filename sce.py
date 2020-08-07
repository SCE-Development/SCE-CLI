import argparse
from tools.setup import SceSetupTool
from tools.sce_presubmit_handler import ScePresubmitHandler

parser = argparse.ArgumentParser()
parser.add_argument(
    'command', help='Setup for the SCE tool to run ' +
    '(setup, run, presubmit, etc.)')
parser.add_argument(
    '--project', '-p', nargs='+', help='Project to run presubmit checks for.')
args = parser.parse_args()

if args.command == 'setup':
    setup = SceSetupTool()
    setup.setup()
if args.command == 'presubmit':
    test_project = ScePresubmitHandler(args.project)
    test_project.handle_testing()
if args.command == 'test':
    setup = SceSetupTool()
    setup.add_sce_alias()
