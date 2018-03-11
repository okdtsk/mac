set -U fish_user_paths $HOME/bin $fish_user_paths

# Load conf.d fish scripts
for file in $HOME/.config/fish/conf.d/*.fish $HOME/.config/fish/conf.user/*.fish
    source $file
end
