source /usr/local/opt/asdf/asdf.fish

# Put each plugins bin path
set ASDF_INSTALLS_PATH /usr/local/opt/asdf/installs
for p in (cat $HOME/.tool-versions | sed 's/ /\//')
  set -x PATH $ASDF_INSTALLS_PATH/$p/bin/ $PATH
end
