#!/bin/bash

function print_repo_nicknames {
    echo
    echo "each repo has nicknames:"
    echo "Clark:clark, dog, clrk, ck, c"
    echo "MongoDB (must have clark installed and linked):mongo, db, mongodb"
    echo "Quasar:quasar, q, idsmile"
    echo "SCE-discord-bot:sce-discord-bot, discord-bot, discord, bot, d"
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

declare -A VALID_REPOS=(
    ["clark"]="Clark"
    ["dog"]="Clark"
    ["clrk"]="Clark"
    ["ck"]="Clark"
    ["c"]="Clark"
    ["cleezy"]="cleezy"
    ["url"]="cleezy"
    ["z"]="cleezy"
    ["mongodb"]="Mongo"
    ["mongo"]="Mongo"
    ["db"]="Mongo"
    ["quasar"]="Quasar"
    ["idsmile"]="Quasar"
    ["q"]="Quasar"
    ["sce-discord-bot"]="SCE-discord-bot"
    ["discord-bot"]="SCE-discord-bot"
    ["discord"]="SCE-discord-bot"
    ["bot"]="SCE-discord-bot"
    ["d"]="SCE-discord-bot"
)

declare -A VALID_COMMANDS=(
    ["link"]=1
    ["clone"]=1
    ["run"]=1
    ["setup"]=1
    ["completion"]=1
    ["create"]=1
)

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

# Checks for valid command
if ! [[ -n "${VALID_COMMANDS[$1]}" ]]; then
    print_usage
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
start_only_mongodb_container=1

# Check for second parameter before proceeding
if [ -z "$2" ]; then
    print_usage
fi

# Every key must have a value as -n checks if value is non-empty string 
if [[ -n "${VALID_REPOS[$2]}" ]]; then
    name=${VALID_REPOS[$2]}

    if [ $name == "Quasar" ]; then
        configPaths+=("config/config.json")

    elif [ $name == "Clark" ]; then
        configPaths+=("src/config/config.json")
        configPaths+=("api/config/config.json")

    elif [ $name == "Mongo" ]; then
        start_only_mongodb_container=0
        name="Clark"
        
    elif [ $name == "SCE-discord-bot" ]; then
        configPaths+=("config.json")
    fi
else
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
    if [ $start_only_mongodb_container == 0 ]
    then
        docker-compose -f docker-compose.dev.yml up mongodb -d
        exit 0
    fi
    if [ $name == "SCE-discord-bot" ]
    then
        docker-compose up --build
        exit 0
    fi
    docker-compose -f docker-compose.dev.yml up --build
    exit 0
fi
