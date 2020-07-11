from tools.setup import SceSetupTool

setup = SceSetupTool()
setup.check_os()
setup.check_docker()
setup.check_mongo()

setup.setup_rpc()
setup.setup_core_v4()
setup.setup_discord_bot()
