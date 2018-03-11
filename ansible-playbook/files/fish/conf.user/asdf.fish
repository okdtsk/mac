source /usr/local/opt/asdf/asdf.fish

for p in (asdf current | grep -v 'No version set' | awk '{print $1}')
    set -x PATH $PATH (dirname (asdf which $p))
end
