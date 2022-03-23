import subprocess

class SceCloneHandler:
	projects = {
		"core-v4": "https://github.com/SCE-Development/Core-v4.git",
		"sce-discord-bot": "https://github.com/SCE-Development/SCE-discord-bot.git",	
		"discord-bot": "https://github.com/SCE-Development/SCE-discord-bot.git",
		"quasar": "https://github.com/SCE-Development/Quasar.git"
	}

	def __init__(self, project) -> None:
		if project == None:
			self.project = ["core-v4"]
		self.project = project

	def print_usage(self):
		print(f"""
		Please enter only one valid project.
		Valid projects are: {list(self.test_commands.keys())}.
		""")

	def handle_cloning(self):
		if(not self.project or len(self.project) != 1 or self.project[0] not in self.projects):
			self.print_usage()
			return
		process = subprocess.Popen(['git', 'clone', self.projects[self.project[0].lower()]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		stdout, stderr = process.communicate()