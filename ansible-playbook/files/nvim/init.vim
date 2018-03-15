" *****
" * ref) https://github.com/kristijanhusak/neovim-config/blob/master/init.vim

" === Plugins {{{
call plug#begin()
Plug 'w0rp/ale'
Plug 'davidhalter/jedi-vim', {'for': 'python'}
Plug 'dracula/vim', {'as': 'dracula'}
Plug 'tpope/vim-fugitive'
Plug 'ntpeters/vim-better-whitespace'
call plug#end()
" }}}

" === General configs
set title
set number
set history=500
set showcmd
set cursorline
set smartcase
set ignorecase
set showmatch
set nostartofline
set fileencoding=utf-8
set wrap
set linebreak
set listchars=tab:\ \ ,trail:·
set list
set lazyredraw
set background=dark
set hidden
set splitright
set splitbelow
set path+=**
set inccommand=nosplit
set fillchars+=vert:\│
set pumheight=30
set exrc
set secure
set grepprg=rg\ --vimgrep
set tagcase=smart
set updatetime=500

" === color
syntax on
color dracula

" === swap file
set noswapfile
set nobackup
set nowb

" === persistent undo
set undodir=~/.config/nvim/backups
set undofile

" === indention
set shiftwidth=2
set softtabstop=2
set tabstop=2
set expandtab
set smartindent
set nofoldenable
set colorcolumn=80
set foldmethod=syntax

" === Auto commands
augroup vimrc
    autocmd!
augroup END
" > Add cursorline highlight in normal mode and remove snippet markers
autocmd vimrc FileType python setlocal sw=4 sts=4 ts=4

" === Statusline
hi User1 guifg=#FF0000 guibg=#425762 gui=bold
hi User2 guifg=#FFFFFF guibg=#FF1111 gui=bold
set statusline=\ %{toupper(mode())}               "Mode
set statusline+=\ \│\ %{fugitive#head()}          "Git branch
set statusline+=\ \│\ %4F                         "File path
set statusline+=\ %1*%m%*                         "Modified indicator
set statusline+=\ %w                              "Preview indicator
set statusline+=\ %r                              "Read only indicator
set statusline+=\ %q                              "Quickfix list indicator
set statusline+=\ %=                              "Start right side layout
set statusline+=\ %{&enc}                         "Encoding
set statusline+=\ \│\ %y                          "Filetype
set statusline+=\ \│\ %p%%                        "Percentage
set statusline+=\ \│\ %c                          "Column number
set statusline+=\ \│\ %l/%L                       "Current line number/Total line numbers
set statusline+=\ %2*%{AleStatusline()}%*         "Errors count

" === Abbreviations
cnoreabbrev Wq wq
cnoreabbrev WQ wq
cnoreabbrev W w
cnoreabbrev Q q
cnoreabbrev Qa qa
cnoreabbrev Bd bd
cnoreabbrev bD bd
cnoreabbrev wrap set wrap
cnoreabbrev nowrap set nowrap
cnoreabbrev bda BufOnly
cnoreabbrev t tabe
cnoreabbrev T tabe
cnoreabbrev f find
cnoreabbrev F find

" === Functions
function! Search(...)
  let default = a:0 > 0 ? expand('<cword>') : ''
  let term = input('Search for: ', default)
  if term != ''
    let path = input('Path: ', '', 'file')
    :execute 'CtrlSF "'.term.'" '.path
  endif
endfunction

function! AleStatusline()
  let count = ale#statusline#Count(bufnr(''))
  let errors = count['error'] ? printf(' %d E ', count['error']) : ''
  let warnings = count['warning'] ? printf(' %d W ', count['warning']) : ''
  let separator = count['error'] && count['warning'] ? '│' : ''

  return printf('%s%s%s', errors, separator, warnings)
endfunction

" *** Plugin configurations
" === jedi-vim "
autocmd FileType python setlocal completeopt-=preview
let g:jedi#force_py_version = 3

" === vim-better-whitespace
let g:better_whitespace_enabled=1
let g:strip_whitespace_on_save=1
let g:strip_whitelines_at_eof=1
let g:show_spaces_that_precede_tabs=1
