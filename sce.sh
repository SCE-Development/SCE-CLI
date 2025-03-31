#!/bin/bash

function print_repo_nicknames {
    echo
    echo "each repo has nicknames:"
    echo "Clark:clark, dog, clrk, ck, c"
    echo "MongoDB (must have clark installed and linked):mongo, db, mongodb"
    echo "Quasar:quasar, q, idsmile"
    echo "SCE-discord-bot:sarah, sce-discord-bot, discord-bot, discord, bot, d"
    echo "cleezy:cleezy url z"
    echo "sceta:sceta, transit"
}

function print_usage {
    echo "usage: sce {clone,run,link,setup} {repo name}"
    echo
    echo "clone: clone the given repo from github."
    echo "run: run the repo using docker"
    echo "link: tell the sce tool where to find the repo on your computer"
    echo "create: create a user for the SCE website"
    echo "setup: copy config.example.json in a repo to config.json"
    print_repo_nicknames
    exit 1
}

function print_missing_config {
    echo
    echo it seems like you forgot to create/configure the config.json file/files
    echo follow the config.example.json as a template and add it at the following paths: 
    for str in ${missingPaths[@]}; do
        echo $(readlink -f $REPO_LOCATION)/$str
    done
    echo
    exit 1
}

function print_repo_not_found {
    echo it looks like you havent linked $1 to the sce tool.
    echo
    echo either link the repo with sce link $1 or clone it first with sce link $1.
    exit 1
}

SCE_COMMAND_DIRECTORY=$(echo $0 | rev |  cut -c7- | rev)
GITHUB_BASE_HTTP_URL="https://github.com/SCE-Development/"
# sce clone <repo> --ssh
# sce clone <repo>
# git@github.com:SCE-Development/Clark.git
GITHUB_BASE_SSH_URL="git@github.com:SCE-Development/"

CLARK_REPO_NAME="Clark"
CLEEZY_REPO_NAME="cleezy"
QUASAR_REPO_NAME="Quasar"
SCE_DISCORD_BOT_REPO_NAME="SCE-discord-bot"
SCETA_REPO_NAME="SCEta"

CLARK_NAMES=("clark" "dog" "clrk" "ck" "c")
CLEEZY_NAMES=("cleezy" "url" "z")
MONGODB_NAMES=("mongo" "db" "mongodb")
QUASAR_NAMES=("quasar" "q" "idsmile")
SCE_DISCORD_BOT_NAMES=("sarah" "sce-discord-bot" "discord-bot" "discord" "bot" "s" "d")
SCETA_NAMES=("sceta" "transit")

VALID_COMMANDS=("link" "clone" "run" "setup" "completion" "create")

function contains_element {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

function contains_config {
    # check file for each path in configPaths
    for str in "${configPaths[@]}"; do 
        if [ ! -f "$str" ]; then
            missingPaths+=($str)
        fi
    done
    if [ ${#missingPaths[@]} -gt 0 ]; then
        return 1
    fi
    return 0
}

function is_quasar_alias {
    result=$(contains_element "$1" "${QUASAR_NAMES[@]}")
    return $result
}

function is_clark_alias {
    result=$(contains_element "$1" "${CLARK_NAMES[@]}")
    return $result
}

function is_cleezy_alias {
    result=$(contains_element "$1" "${CLEEZY_NAMES[@]}")
    return $result
}

function is_mongodb_alias {
    result=$(contains_element "$1" "${MONGODB_NAMES[@]}")
    return $result
}

function is_discord_bot_alias {
    result=$(contains_element "$1" "${SCE_DISCORD_BOT_NAMES[@]}")
    return $result
}

function is_sceta_alias {
    result=$(contains_element "$1" "${SCETA_NAMES[@]}")
    return $result
}

function is_valid_command {
    result=$(contains_element "$1" "${VALID_COMMANDS[@]}")
    return $result
}

is_valid_command "$1"
if [ $? -eq 1 ] 
then  
    print_usage
    exit 1
fi

if [ $1 == "completion" ]
then
    if [ -n "$FISH_VERSION" ]; then
        # Fish shell detected
        echo "function sce; bash $(pwd)/sce.sh \$argv; end"
        exit 0
    fi
    # For other shells (Bash, Zsh, etc.)
    echo "# for the sce dev tool"
    echo "alias sce=\"$(pwd)/sce.sh\""
    echo ""
    exit 0
fi

if [ $1 == "create" ]
then
    cat $SCE_COMMAND_DIRECTORY"create_user.txt" | docker exec -i sce-mongodb-dev mongosh --shell --norc --quiet
    exit 0
fi

name=""
configPaths=()
missingPaths=()
is_quasar_alias "$2"
if [ $? -eq 0 ]
then
    name=$QUASAR_REPO_NAME
    configPaths+=("config/config.json")
fi

is_clark_alias "$2"
if [ $? -eq 0 ]
then
    name=$CLARK_REPO_NAME
    configPaths+=("src/config/config.json")
    configPaths+=("api/config/config.json")
fi

is_cleezy_alias "$2"
if [ $? -eq 0 ]
then
    name=$CLEEZY_REPO_NAME
fi

is_mongodb_alias "$2"
start_only_mongodb_container=$?
if [ $start_only_mongodb_container -eq 0 ]
then
    name=$CLARK_REPO_NAME
fi

is_discord_bot_alias "$2"
if [ $? -eq 0 ]
then
    name=$SCE_DISCORD_BOT_REPO_NAME
    configPaths+=("config.json")
fi

is_sceta_alias "$2"
if [ $? -eq 0 ]
then
    name=$SCETA_REPO_NAME
fi

if [ -z "$name" ]
then
    print_usage
fi

if [ $1 == "clone" ]
then
    # clone with the SSH URL if the user wanted to
    # if the third argument is absent or anything else
    # just default to the HTTPS url
    if [[ ! -z "$3" ]] && [[ $3 == "--ssh" ]]
    then
        git clone "$GITHUB_BASE_SSH_URL$name.git"
    else
        git clone "$GITHUB_BASE_HTTP_URL$name.git"
    fi
    exit 0
elif [ $1 == "link" ]
then
    sce_run_location=$(pwd)
    # remove sim link if it exists, ignore any stderr/stdout
    rm "$SCE_COMMAND_DIRECTORY$name" &> /dev/null
    ln -s "$sce_run_location" "$SCE_COMMAND_DIRECTORY$name"
elif [ $1 == "run" ]
then
    REPO_LOCATION="$SCE_COMMAND_DIRECTORY$name"
    if [ ! -d "$REPO_LOCATION" ] 
    then
        print_repo_not_found $name
    fi
    cd $REPO_LOCATION
    contains_config $configPaths
    if [ $? -eq 1 ]
    then
        print_missing_config $REPO_LOCATION $missingPaths
    fi
    if [ $start_only_mongodb_container -eq 0 ]
    then
        docker-compose -f docker-compose.dev.yml up mongodb -d
        exit 0
    fi
    docker-compose -f docker-compose.dev.yml up --build
    exit 0
fi
