# SCE Development Environment
To work on any of the SCE projects, clone this repository and run
 `python3 sce.py setup`.

## Available Commands
### Setup
This will clone and setup [Core-v4](https://github.com/SCE-Development/Core-v4/) and 
 [SCE-discord-bot](https://github.com/SCE-Development/SCE-discord-bot).
 This command can be run with `python3 sce.py setup` for MacOS/Linux or `py sce.py setup` for Windows.

The tool will automatically create a `sce` command which you can run from anywhere.

**Note:** For windows users, you will be prompted to add this to your path for the `sce` command.
![image](https://user-images.githubusercontent.com/36345325/89665917-4acb1400-d88e-11ea-97d8-1ace95b5741f.png)


### Presubmit
This tool runs presubmit checks for a project. For example:
```sh
# To run tests on all projects
sce presubmit
```

### Run
This command will run a number of services for development. The available commands are:
```sh
# runs everything
sce run
# runs the core-v4 frontend
sce run frontend
# runs the core-4 backend server
sce run server
# runs the discord bot project
sce run discord
# runs the core-v4 project
sce run core-v4
# runs mongod
sce run mongo
```
**Note:** you can run multiple services at once e.g. `npm run discord server`

### Rebuild
This is for Windows users only, who need to rebuild their `.exe` file for the
 `sce` command to work.
```
sce rebuild
```
