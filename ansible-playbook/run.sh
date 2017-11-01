#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [ ! -e ./playbook-each-environment.yml ]; then
    echo "---" > ./playbook-each-environment.yml
fi

ansible-playbook -i hosts ./playbook.yml $@
