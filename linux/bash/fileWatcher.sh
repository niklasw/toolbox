#!/bin/bash

watchedFile=$1

while true
do
    inotifywait -e access $watchedFile \
    && echo "file access -- $(date)"
done

