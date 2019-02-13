#!/bin/bash

# script to fetch latest code from automation scripts repo

function tryexec() {
     cmd=$1
     for x in {{1..1}}; do
       eval $cmd
       if [[ $? -eq 0 ]]; then
         return
       fi
    done
    echo "Failed to execute $cmd"
    exit 1
 }

cd $WORKSPACE/automationscripts
tryexec git fetch
tryexec git reset --hard origin/master

# time to run deploy production script
tryexec ./projects/pdns_ui/pdnsui_prod.sh
