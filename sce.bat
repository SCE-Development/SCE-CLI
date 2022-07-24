@echo off

setlocal ENABLEDELAYEDEXPANSION

REM aliases for the sce dev projects
set COREV4_PTIONS="core-v4" "corev4" "cv4" "c4" "c"
set QUASAR_OPTIONS="quasar" "q" "idsmile"
set DISCORD_BOT_OPTIONS="sce-discord-bot" "discord-bot" "discord" "bot" "d"
set GITHUB_BASE_URL=https://github.com/SCE-Development/
set COREV4_REPO_NAME=Core-v4
set QUASAR_REPO_NAME=Quasar
set SCE_DISCORD_BOT_REPO_NAME=SCE-discord-bot

REM parse two very important things. 1. find where the script was ran from
REM in the command line, 2. where the script is located on the user's disk
FOR /F "tokens=*" %%g IN ('where ecs.bat') do (SET SCE_SCRIPT_LOCATION=%%g)
FOR /F "tokens=*" %%g IN ('cd') do (SET WHERE_COMMAND_WAS_RAN_FROM=%%g)

REM this yields the location of where the sce command line
REM is installed. for example if the batch script lives
REM in D:\user\sce\sce.bat, the below variable will have
REM the value D:\user\sce\
REM for more info on substrings in batch: https://stackoverflow.com/a/47989051
SET SCE_COMMAND_DIRECTORY=!SCE_SCRIPT_LOCATION:~0,-7!

REM the usage for the sce command line tool is
REM sce <run/link/clone> <repo name>. these command line
REM arguments are referenced as %1% and %2% respectively.
IF "%1%"=="link"  (
    goto :extract_repo_name
) ELSE IF "%1%"=="clone" (
    goto :extract_repo_name
) ELSE IF "%1%"=="run" (
    goto :extract_repo_name
) ELSE IF "%1%"=="setup" (
    goto :extract_repo_name
) ELSE (
    goto :print_usage
)

REM Resolve the given repo name from the user to actual repo name. 
REM We iterate over the possible nicknames for each project and then
REM set the varible %name% to the resolved repo. 
:extract_repo_name
    REM check if argument is set https://stackoverflow.com/a/830566
    if "%2%" == "" (
        goto :print_command_usage
    )
    REM comparing variable with a bunch of values:
    REM https://stackoverflow.com/a/38481845
    SET name=""
    SET repo_to_link="%2%"
    (for %%a in (%COREV4_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%COREV4_REPO_NAME%
            goto :%1%
        )
    ))
    (for %%a in (%QUASAR_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%QUASAR_REPO_NAME%
            goto :%1%
        )
    ))
    (for %%a in (%DISCORD_BOT_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%SCE_DISCORD_BOT_REPO_NAME%
            goto :%1%
        )
    ))
    goto :print_command_usage

:link
    SET NEW_JUNCTION=%SCE_COMMAND_DIRECTORY%%name%
    REM try deleting any existing junction to the repo.
    REM we hide the output of this command just in case
    REM the junction does not exist.
    REM see https://stackoverflow.com/a/1262726
    rmdir %NEW_JUNCTION% > nul 2>&1
    REM mklik /j <JUNCTION U WANNA CREATE> <ORIGINAL LOCATION>
    SET mklik_params=%NEW_JUNCTION% %WHERE_COMMAND_WAS_RAN_FROM%
    mklink /j %mklik_params%
    goto :exit_success

:setup
    REM run the docker container  
    SET REPO_LOCATION=%SCE_COMMAND_DIRECTORY%%name%
    REM if location doesnt exist, prompt the user to link the directory
    REM copy api\config\config.example.json  api\config\config.json
    REM copy src\config\config.example.json  src\config\config.json
    IF NOT EXIST %REPO_LOCATION% (
        goto :print_repo_not_found
    )
    cd %REPO_LOCATION%
    if %name%==%COREV4_REPO_NAME% (
        copy api\config\config.example.json  api\config\config.json
        copy src\config\config.example.json  src\config\config.json
    ) else if %name%==%QUASAR_REPO_NAME% (
        copy config\config.example.json  config\config.json
    ) else if %name%==%SCE_DISCORD_BOT_REPO_NAME% (
        copy config.example.json config.json
    )
    goto :exit_success

:clone
    REM clone the repo via HTTPS, note that the end of every 
    REM GitHub repo url has a ".git" so we append it below.
    git clone "%GITHUB_BASE_URL%%name%.git"
    goto :exit_success

:run
    REM run the docker container  
    SET REPO_LOCATION=%SCE_COMMAND_DIRECTORY%%name%
    REM if location doesnt exist, prompt the user to link the directory
    IF NOT EXIST %REPO_LOCATION% (
        goto :print_repo_not_found
    )
    cd %REPO_LOCATION%
    docker-compose -f docker-compose.dev.yml up
    goto :exit_success

:print_command_usage
    echo usage: sce %1% {repo name}
    goto :print_repo_nicknames

:print_usage
    echo usage: sce {clone,run,link,setup} {repo name}
    echo.
    echo clone: clone the given repo from github.
    echo run: run the repo using docker
    echo link: tell the sce tool where to find the repo on your computer
    echo setup: copy config.example.json in a repo to config.json
    goto :print_repo_nicknames

:print_repo_nicknames
    echo.
    echo each repo has nicknames:
    echo Core-v4:core-v4, corev4, cv4, c4, c
    echo Quasar:quasar, q, idsmile
    echo SCE-discod-bot:sce-discord-bot, discord-bot, discord, bot, d
    REM assumes this was printed when the user incorrectly used the command
    goto :exit_error

:print_repo_not_found
    echo it looks like you havent linked %name% to the sce tool.
    echo.
    echo either link the repo with `sce link %name% or clone it first with sce link %name%.
    goto :exit_error 

:exit_error
    EXIT /B 1

:exit_success
    EXIT /B 0
