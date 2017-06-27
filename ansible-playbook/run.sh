#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

ansible-playbook -i hosts ./playbook.yml $@
