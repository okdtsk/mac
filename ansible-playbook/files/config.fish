set -U fish_user_paths $HOME/bin $fish_user_paths

set -x JAVA_HOME (/usr/libexec/java_home -v 1.8)

source ~/.config/fish/iterm2_shell_integration.fish

set -x EDITOR /usr/local/bin/vim
eval (direnv hook fish)

complete --command aws --no-files --arguments '(begin; set --local --export COMP_SHELL fish; set --local --export COMP_LINE (commandline); aws_completer | sed \'s/ $//\'; end)'

function gcd
    if count $argv > /dev/null
        set path (ghq list --full-path | fzf -1 -q $argv)
    else
        set path (ghq list --full-path | fzf -1)
    end
    cd $path
end

set -x GOPATH ${HOME}/go

set -x PATH ${PATH} ${GOPATH}/bin

