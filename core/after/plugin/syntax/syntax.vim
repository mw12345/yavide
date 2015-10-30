" Vim syntax file
" Language:	C++
"
" Ideas borrowed from: http://stackoverflow.com/questions/736701/class-function-names-highlighting-in-vim

" Functions
syn match   cCustomParen    "?=(" contains=cParen contains=cCppParen
syn match   cCustomFunc     "\w\+\s*(\@=" contains=cCustomParen
syn match   cCustomScope    "::"
syn match   cCustomClass    "\w\+\s*::" contains=cCustomScope

hi def link cCustomFunc  Function
hi def link cCustomClass Function

source after/syntax/tags-macro.vim
source after/syntax/tags-class.vim
source after/syntax/tags-struct.vim
source after/syntax/tags-enum.vim
source after/syntax/tags-union.vim
source after/syntax/tags-typedef.vim

