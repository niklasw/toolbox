#!/usr/bin/env bash


function push_branch_to_github() {
    git push --set-upstream origin "$(git rev-parse --abbrev-ref HEAD)"
}

function pull_branch_from_github() {
    git pull origin "$(git rev-parse --abbrev-ref HEAD)"
}

function git_pull_new_branch_from_github() {
    local branch_name="$1"
    git checkout -b "$branch_name" "origin/$branch_name"
}

