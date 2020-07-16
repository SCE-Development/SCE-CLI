import argparse
from tools.setup import SceSetupTool

setup = SceSetupTool()
parser = argparse.ArgumentParser()

parser.add_argument('--setup', dest='setup', action='store_true')
args = parser.parse_args()

if args.setup:
    setup.check_os()
    setup.check_docker()
    setup.check_mongo()

    setup.setup_rpc()
    setup.setup_core_v4()
    setup.setup_discord_bot()
else:
    print('did nothing wrong')
