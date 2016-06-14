title: Installing haskell on linux
date: 2016-06-14 11:30
tags: haskell, linux
category: haskell
slug: installing-haskell-on-linux
author: Chris Perivolaropoulos

If for some reason you don't want to use your distribution's package
manager (eg because it provides an outdated version of GHC), run the
following:

    wget https://haskell.org/platform/download/8.0.1/haskell-platform-8.0.1-unknown-posix--minimal-i386.tar.gz -O /tmp/haskell.tar.gz
    cd /tmp
    tar xvzf /tmp/haskell.tar.gz
    sudo ./install-haskell-platform.sh

And restart your shell. The above is just a copy-paste-able format of
the instructions in
[haskell.org](https://www.haskell.org/platform/linux.html#linux-generic)
