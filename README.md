# SCE Development Environment
Command line tool to run any of the SCE projects. Works on Windows, Mac and
 Linux. Available with the `sce` command.

## Prerequisites

- [Docker](https://www.docker.com/)

## Setup

### Mac/Linux

Install with one command:
```sh
curl -sSL https://raw.githubusercontent.com/SCE-Development/SCE-CLI/master/install.sh | sh
```

This downloads the correct binary for your system and installs it to `/usr/local/bin/sce`.

### Windows

Run in PowerShell:
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SCE-Development/SCE-CLI/master/install.ps1" -UseBasicParsing | Invoke-Expression
```

### Verify

After installing, open a new terminal and run:
```
sce --help
```

## Usage
Use the command `sce` with a command and repo name.
Run `sce --help` to see all available commands.

### Repo Names
Each repo has nicknames you can use interchangeably:

| Repo | Nicknames |
|------|-----------|
| Clark | clark, dog, clrk, ck, c |
| MongoDB | mongo, db, mongodb |
| Quasar | quasar, q, idsmile |
| SCE-discord-bot | sarah, sce-discord-bot, discord-bot, discord, bot, s, d |
| cleezy | cleezy, url, z |
| SCEta | sceta, transit |

### Clone
Clone an SCE project from GitHub:
```
sce clone <project> [--ssh]
```
The `--ssh` flag clones using the SSH URL instead of HTTPS.

### Link
Link a repo directory to the sce tool (run from inside the repo):
```
sce link <project>
```

### Run
Run an SCE project with Docker:
```
sce run <project>
```
To start only MongoDB:
```
sce run db
```

### Setup
Copy config.example.json to config.json for a project:
```
sce setup <project>
```

### Create
Create a test account for the SCE website. Make sure MongoDB is running first:
```
sce run db
```
Then create a user:
```
sce create [level]
```
Levels: `admin` (default), `officer`, `member`, `nonmember`, `pending`, `banned`.

Log in with the generated email and password `sce`.

### Lint
Run eslint --fix on running containers (Clark and SCE-discord-bot only):
```
sce lint <project>
```
Make sure the project is running with `sce run` first.
