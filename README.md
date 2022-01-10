# SCE Development Environment
To work on any of the SCE projects, clone this repository and run
 `python3 sce.py setup`.

## Setup
This will clone and setup [Core-v4](https://github.com/SCE-Development/Core-v4/) and 
 [SCE-discord-bot](https://github.com/SCE-Development/SCE-discord-bot),
 as well as allow the command `sce` to be ran from the terminal.

### Windows
Before starting, ensure you have python3 installed and the
 launcher option was selected at the time of setup (check the second to
 bottom box!):

![image](https://docs.python.org/3/_images/win_installer.png)

**Note:** You may get an error asking you to install the Visual Studio build
 tools. A link to download is
 [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).


Afterwards, ensure you have the launcher installed by running 
 this in your terminal:
```sh
py --version
```

You should not get an error but instead the version given to you e.g. `Python 3.X.X`

You can now setup the tool with
```
py sce.py setup
```

For windows users, you will be prompted to add this to your path for the `sce` command.
![image](https://user-images.githubusercontent.com/36345325/89665917-4acb1400-d88e-11ea-97d8-1ace95b5741f.png)

To do this open your control panel and search "path":
![image](https://user-images.githubusercontent.com/63386979/148730177-dd7fd6a7-c854-4bbc-8f11-53fe36b8327b.png)

Select `Edit environment variables for your account`. You should
 be taken to the below view where you should paste the path (see bottom
 entry in below screenshot).

![image](https://user-images.githubusercontent.com/63386979/148730277-643b0f9c-74d6-45d0-a273-e7ef836d9db8.png)

You should now be good to go! Reload your VS Code window and open a
 new terminal. The command `sce` should work now.

### Mac/Linux
Ensure you have python3 installed!

Then, simply run

```sh
python3 sce.py setup
```

After reloading your terminal, the `sce` command should work.

## Available Commands

### Presubmit
This tool runs presubmit checks for a project. For example:
```sh
# To run tests on all projects
sce presubmit -p <project name>
```

Available project names are `Core-v4`, `SCE-discord-bot` and `dev`. So to run
 presubmit checks for Core-v4, we would do:
```sh
sce presubmit -p Core-v4
```

### Run
This command will run a number of services for development.  For example:
```sh
sce run -s <service name>
```
Available service names are:

- `frontend`: core-v4 frontend
- `server`: core-4 backend server
- `discord`: discord bot project
- `core-v4`: core-v4 project
- `mongo`: mongodb on port 27017

**Note:** you can run multiple services at once e.g.

```sh
# runs the discord bot and core-v4 backend
sce run -s discord server
```

If you wanted to run everything at once, do:

```sh
sce run
```
