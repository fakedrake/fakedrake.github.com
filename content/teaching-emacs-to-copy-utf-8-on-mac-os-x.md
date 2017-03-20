title: Teaching emacs to copy utf-8 on Mac OS X
date: 2016-05-12 16:48
tags: emacs, macosx
category: emacs
slug: teaching-emacs-to-copy-utf-8-on-mac-os-x
author: Chris Perivolaropoulos

Mac OS X comes with a command line tool for maniplating the clipboard
called `pbcopy`. It's usage is simple: you throw stuff in it's stdin
and that stuff is copied to the clipboard. This way we can teach emacs
to copy stuff to the clipboard with this function


    :::lisp
    (defun paste-to-osx (text &optional push)
      (let ((process-connection-type nil)
            (default-directory "~"))
        (let ((proc (start-process "pbcopy" "*Messages*" "pbcopy")))
          (process-send-string proc text)
          (process-send-eof proc))))


    (setq interprogram-cut-function 'paste-to-osx)

And this will work pretty well for englshIf you. It will however fail
in other languages. For example copying the string `λογος, αιμα,
νοημα` from an emacs buffer will paste as random unicode characeters.

Setting the `LANG` env var fixes the problem.

    (defun paste-to-osx (text &optional push)
      (let ((process-connection-type nil)
            (lang (getenv "LANG"))
            (default-directory "~"))
        (setenv "LANG" "en_US.UTF-8")
        (let ((proc (start-process "pbcopy" "*Messages*" "pbcopy")))
          (process-send-string proc text)
          (process-send-eof proc))
        (setenv "LANG" lang)))
