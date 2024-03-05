#!/bin/bash

_sce_completion() {
    local cur prev opts repos
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="clone run link setup completion"
    repos="Clark cleezy Quasar SCE-discord-bot SCEta"

    if [[ ${prev} == "clone" || ${prev} == "run" || ${prev} == "link" ]]; then
        COMPREPLY=( $(compgen -W "${repos}" -- ${cur}) )
    else
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    fi

    if [[ ${#COMPREPLY[@]} -eq 0 ]]; then
        COMPREPLY=( $(compgen -o default -- ${cur}) )
    fi

    return 0
}
complete -F _sce_completion sce
