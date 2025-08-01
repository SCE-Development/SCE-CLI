@echo off

setlocal ENABLEDELAYEDEXPANSION

REM aliases for the sce dev projects
set CLARK_OPTIONS="clark" "clrk" "ck" "c"
set CLEEZY_OPTIONS="cleezy" "url" "z"
set MONGODB_OPTIONS="mongo" "db" "mongodb"
set QUASAR_OPTIONS="quasar" "q" "idsmile"
set DISCORD_BOT_OPTIONS="sarah" "discord-bot" "discord" "bot" "s" "d"
set SCETA_OPTIONS="sceta" "transit"
set GITHUB_BASE_URL=https://github.com/SCE-Development/
set CLARK_REPO_NAME=Clark
set CLEEZY_REPO_NAME=cleezy
set QUASAR_REPO_NAME=Quasar
set SCE_DISCORD_BOT_REPO_NAME=sarah
set SCETA_REPO_NAME=SCEta
REM parse the location where:
REM 1. the `sce` command was ran from in the command line
REM 2. the actual sce.bat script is located on the user's disk
FOR /F "tokens=*" %%g IN ('where sce.bat') do (SET SCE_SCRIPT_LOCATION=%%g)
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
) ELSE IF "%1%"=="create" (
    goto :create_mongodb_user
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
    set is_mongodb_alias=""
    SET repo_to_link="%2%"
    (for %%a in (%CLARK_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%CLARK_REPO_NAME%
            SET CONFIG_LOCATION[1]=src\config\config.json
            SET CONFIG_LOCATION[2]=api\config\config.json
            SET CONFIG_LOCATION_LENGTH=2
            goto :%1%
        )
    ))
    (for %%a in (%CLEEZY_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%CLEEZY_REPO_NAME%
            goto :%1%
        )
    ))
    (for %%a in (%MONGODB_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%CLARK_REPO_NAME%
            SET is_mongodb_alias="true"
            goto :%1%
        )
    ))
    (for %%a in (%QUASAR_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%QUASAR_REPO_NAME%
            SET CONFIG_LOCATION[1]=config\config.json
            SET CONFIG_LOCATION_LENGTH=1
            goto :%1%
        )
    ))
    (for %%a in (%DISCORD_BOT_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%SCE_DISCORD_BOT_REPO_NAME%
            SET CONFIG_LOCATION[1]=config.json
            SET CONFIG_LOCATION_LENGTH=1
            goto :%1%
        )
    ))
    (for %%a in (%SCETA_OPTIONS%) do (
        if %repo_to_link% == %%a (
            SET name=%SCETA_REPO_NAME%
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
    if %name%==%CLARK_REPO_NAME% (
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


    REM change directory from junction path to actual/target path
    REM fsutil reparsepoint query returns an output similar to below that we must parse through

    REM Reparse Tag Value : 0xa0000003
    REM Tag value: Microsoft
    REM Tag value: Name Surrogate
    REM Tag value: Mount Point
    REM Substitue Name offset: 0
    REM Substitue Name length: 68
    REM Print Name offset:     70
    REM Print Name Length:     60
    REM Substitute Name:       \??\C:\path\to\Clark
    REM Print Name:            C:\path\to\Clark
    REM Reparse Data Length: 0x8c
    REM Reparse Data:
    REM 0000:  00 00 44 00 46 00 3c 00  5c 00 3f 00 3f 00 5c 00 
    REM 0010:  43 00 3a 00 5c 00 55 00  73 00 65 00 72 00 73 00  
    REM 0020:  5c 00 63 00 6a 00 6c 00  6f 00 75 00 5c 00 44 00 
    REM 0030:  6f 00 63 00 75 00 6d 00  65 00 6e 00 74 00 73 00
    REM 0040:  5c 00 43 00 6c 00 61 00  72 00 6b 00 00 00 43 00
    REM 0050:  3a 00 5c 00 55 00 73 00  65 00 72 00 73 00 5c 00
    REM 0060:  63 00 6a 00 6c 00 6f 00  75 00 5c 00 44 00 6f 00 
    REM 0070:  63 00 75 00 6d 00 65 00  6e 00 74 00 73 00 5c 00 
    REM 0080:  43 00 6c 00 61 00 72 00  6b 00 00 00   

    REM get the line with the prefix "Print Name:            " and set it to REAL_PATH
    FOR /f "tokens=* USEBACKQ" %%a IN (`fsutil reparsepoint query %REPO_LOCATION% ^| findstr "Print Name:"`) DO (
        SET REAL_PATH=%%a
    )
    REM remove the prefix "Print Name:            " from REAL_PATH leaving only the target path
    SET "REAL_PATH=!REAL_PATH:Print Name:            =!"
    REM change directory into the target path
    cd /d "!REAL_PATH!"

    REM Check if config file exists before running
    CALL :check_config_file
    IF NOT "!MISSING_PATHS_LENGTH!"=="0" (

        goto :print_missing_config
    )
    IF %is_mongodb_alias%=="true" (
        docker-compose -f docker-compose.dev.yml up mongodb -d
        goto :exit_success
    )
    docker-compose -f docker-compose.dev.yml up --build
    goto :exit_success

:create_mongodb_user
    type %SCE_COMMAND_DIRECTORY%create_user.txt | docker exec -i sce-mongodb-dev mongosh --quiet --norc --shell
    echo created admin user for the SCE website with:
    echo email:    test@one.sce
    echo password: sce
    goto :exit_success

:check_config_file

    SET MISSING_PATHS_LENGTH=0
    FOR /L %%a IN (1,1,%CONFIG_LOCATION_LENGTH%) DO (
        IF NOT EXIST ".\!CONFIG_LOCATION[%%a]!" (
            SET /A MISSING_PATHS_LENGTH+=1
            SET MISSING_PATHS[!MISSING_PATHS_LENGTH!]=!CONFIG_LOCATION[%%a]!
        )
    )
    exit /B 0

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
    echo Clark:clark, clrk, ck, c
    echo MongoDB:mongo, db, mongodb
    echo Quasar:quasar, q, idsmile
    echo Cleezy:cleezy url z
    echo sarah:sarah, sce-discord-bot, discord-bot, discord, bot, s, d
    echo SCEta:sceta, transit
    REM assumes this was printed when the user incorrectly used the command
    goto :exit_error

:print_repo_not_found
    echo it looks like you havent linked %name% to the sce tool.
    echo.
    echo either link the repo with `sce link %name% or clone it first with sce link %name%.
    goto :exit_error 

:print_missing_config
    REM Get real path to config file from symlink
    REM The below fsutil command prints out a bunch of stuff related to the 
    REM The line we are looking for looks like this
    REM Print Name:            E:\vs\temp2\Quasar
    REM This line referes to the acutual directory location, and we want
    REM to parse this line and tell the user where they need to make a config file
    FOR /f "tokens=*" %%a IN ('fsutil reparsepoint QUERY %REPO_LOCATION% ^| FINDSTR "Print Name: "') DO (
        SET "REAL_PATH=%%a"
    )
    SET "REAL_PATH=!REAL_PATH:Print Name:            =!"
    echo.
    echo it seems like you forgot to create/configure the config.json file
    echo follow the config.example.json as a template and add it at the following paths:
    FOR /L %%a IN (1,1,%MISSING_PATHS_LENGTH%) DO (
        echo %REAL_PATH%\!MISSING_PATHS[%%a]!
    )
    echo.
    goto :exit_error

:exit_error
    EXIT /B 1

:exit_success
    EXIT /B 0
