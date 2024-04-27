# SCE Development Environment
Command line tool to run any of the SCE projects. Works on Windows, Mac and
 Linux. Available with the `sce` command.

## Setup
Before starting, be sure you have Docker installed! This tool
 runs SCE's projects with Docker.

Clone this repository to your computer with
```
git clone https://github.com/SCE-Development/SCE-CLI.git
```
Next, we will add the `sce` command to your terminal.

### Windows
You will need to add the location where the batch file is to your path. To do
 this:
1. Copy the path where `SCE-CLI` is installed. The path should look like
```
C:\Users\<username>\path\to\SCE-CLI\
```
2. We need to edit (your env vars or something) we can do this with:
- Press `Window + R` to open the Windows Run prompt.
- Type in `sysdm.cpl` and click `OK`.
![image](https://phoenixnap.com/kb/wp-content/uploads/2021/04/setting-environment-variables-in-windows-06.png)
- Then go to the `Advanced` tab and click `Environment Variables`:
![image](https://phoenixnap.com/kb/wp-content/uploads/2021/04/setting-environment-variables-in-windows-07.png)
- Click on path in `System variables`
![edit_path](https://user-images.githubusercontent.com/10038262/180634975-6a7c7947-5560-4df6-bd5a-3d8bda033c70.png)
- Add the location where `SCE-CLI` is installed from earlier into
 this path (see highlighted)
![path](https://user-images.githubusercontent.com/10038262/180634962-abd4ba91-30a2-47e7-8c50-4cc26a41b669.png)
3. After doing so, typing `sce` in the Command Prompt
 should work, and the help page should show like below:
![eb2015026b076e7b31a8caa2ff8f2e55](https://user-images.githubusercontent.com/10038262/180635207-2ea70c08-003f-4f59-95f8-35817bc6a51b.png)

### Mac/Linux
1. cd into the `SCE-CLI`
2. Add an alias to your terminals config file like:
```sh
# for linux
./sce.sh completion >> ~/.bashrc

# for mac
./sce.sh completion >> ~/.zshrc
```
3. After doing the above, making a new terminal and typing `sce` should work.

## Usage
To use the script, you use the command `sce` with a command and repo name
The commands that you can run are: clone, link, run.
Alternatively, just run the command `sce` to see the usages in the terminal.
### Repo Names
The name of the repositories are (the nicknames are alternate names you can use in the command):
core-v4 (nicknames: core-v4, corev4, cv4, c4, c) 
quasar (nicknames: quasar, q, idsmile)
sce-discord-bot (nicknames: sce-discord-bot, discord-bot, discord, bot, d)

### Clone
To clone an SCE project from GitHub, simply enter
```
sce clone <project> [--ssh]
```
The reposity will be cloned from wherever the command was ran.
Project names can be `quasar`, `core-v4`, `discord` etc. See the above repo
 names section for all options.

The `--ssh` parameter can be optionally added after the project name.
 Supplying this will clone the repo with the GitHub SSH URL over the
 HTTPS one.

### Link
To link a sce repo to your directory where you are running the command, simply enter
```
sce link <project>
```
Project names can be `quasar`, `core-v4`, `discord` etc. See the above repo
 names section for all options.

### Run
To run an SCE project, simply enter

```
sce run <project>
```
where project can be `quasar`, `core-v4`, `discord` etc. See the above repo
 names section for all options.

### Create
This will create a test account when running the SCE website locally. Before running,
 make sure you have MongoDB running with:
```
sce run db
```
Then, run the below command:
```
sce create
```
After running the SCE website locally, ensure you can log in with the email
 `test@one.sce` and password `sce`



