#!/bin/bash

readonly ANSIBLE_OPTS="${@}"

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [ ! -e ./playbook-each-environment.yml ]; then
    echo "---" > ./playbook-each-environment.yml
fi

ansible-playbook -i hosts ${ANSIBLE_OPTS} ./playbook.yml $@
