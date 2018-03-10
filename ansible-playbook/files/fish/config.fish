set -U fish_user_paths $HOME/bin $fish_user_paths

set -x JAVA_HOME (/usr/libexec/java_home -v 1.8)

source ~/.config/fish/iterm2_shell_integration.fish

set -x EDITOR /usr/local/bin/vim
eval (direnv hook fish)


# Load conf.d fish scripts
for file in $HOME/.config/fish/conf.d/*.fish $HOME/.config/fish/conf.user/*.fish
    source $file
end
