function gcd
    if count $argv > /dev/null
        set path (ghq list --full-path | fzf -1 -q $argv)
    else
        set path (ghq list --full-path | fzf -1)
    end
    cd $path
end
