#!/bin/sh

logging() {
  echo "[$(date)] $@"
}

logging "Boostrapping ..."

trap 'ret=$?; test $ret -ne 0 && printf "failed\n\n" >&2; exit $ret' EXIT

set -e

# Ensure Apple's command line tools are installed
if ! command -v cc >/dev/null; then
  logging "Installing xcode ..."
  xcode-select --install
else
  logging "Xcode already installed. Skipping."
fi

if ! command -v brew >/dev/null; then
  logging "Installing Homebrew..."
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" </dev/null
else
  logging "Homebrew already installed. Skipping."
fi

if ! command -v ansible >/dev/null; then
  logging "Installing Ansible ..."
  brew install ansible
else
  logging "Ansible already installed. Skipping."
fi

if ! command -v ghq >/dev/null; then
  logging "Installing ghq ..."
  brew install ghq
else
  logging "Ansible already installed. Skipping."
fi

ghq get https://github.com/okdtsk/mac
cd $(ghq root)/github.com/okdtsk/mac
cd ansible-playbook

logging "Running ansible playbook ..."
./run.sh
