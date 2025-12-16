#!/usr/bin/env sh
source ./az-variables.hide
az login
az batch account login -n $AZ_STORAGE_ACCOUNT -g $AZ_STORAGE_RG
