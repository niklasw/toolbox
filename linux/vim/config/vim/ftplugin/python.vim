" Python
"au BufRead *.py compiler nose
"au FileType python set omnifunc=pythoncomplete#Complete
setlocal expandtab shiftwidth=4 tabstop=8 softtabstop=4 smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class,with
set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m
" Don't let pyflakes use the quickfix window
"let g:pyflakes_use_quickfix = 0

nnoremap <leader>l :lvim /<C-R><C-W>/ *.py<CR>:lw<CR>

