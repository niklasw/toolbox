" Python
"au BufRead *.py compiler nose
"au FileType python set omnifunc=pythoncomplete#Complete
setlocal expandtab shiftwidth=4 tabstop=8 softtabstop=4 smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class,with
set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m
" Don't let pyflakes use the quickfix window
"let g:pyflakes_use_quickfix = 0

nnoremap <leader>l :lvim /<C-R><C-W>/ *.py<CR>:lw<CR>

map <buffer> <F5> :w<CR>:exec '!clear; python3' shellescape(@%, 1)<CR>
imap <buffer> <F5> <esc>:w<CR>:exec '!clear; python3' shellescape(@%, 1)<CR>
map <buffer> <F6> :w<CR>:PymodeRun<CR>
map <buffer> <F7> :PymodeLint<CR>
nnoremap <leader>p :wa<CR>:!python3 -W ignore %<CR>
" autocmd FileType python map <buffer> <F9> :w<CR>:exec '!python3' shellescape(@%, 1)<CR>
" autocmd FileType python imap <buffer> <F9> <esc>:w<CR>:exec '!python3' shellescape(@%, 1)<CR>

let g:pymode_options = 0
let g:pymode_virtualenv=1
