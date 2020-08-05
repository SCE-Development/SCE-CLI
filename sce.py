import argparse
from tools.setup import SceSetupTool

parser = argparse.ArgumentParser()

parser.add_argument(
    'command', help='Setup for the SCE tool to run ' +
    '(setup, run, presubmit, etc.)')
args = parser.parse_args()

if args.command == 'setup':
    setup = SceSetupTool()
    setup.setup()
