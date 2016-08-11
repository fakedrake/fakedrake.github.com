title: Installing haskell on linux
date: 2016-06-14 11:30
tags: haskell, linux
category: haskell
slug: installing-haskell-on-linux
author: Chris Perivolaropoulos

If for some reason you don't want to use your distribution's package
manager (eg because it provides an outdated version of GHC), you can
install it manually. First you need to find out if you are on x64 or
32bit architecture. You can do that by running:

    uname -a

If you are on 32bit run the following:

    wget https://haskell.org/platform/download/8.0.1/haskell-platform-8.0.1-unknown-posix--minimal-i386.tar.gz -O /tmp/haskell.tar.gz
    cd /tmp
    tar xvzf /tmp/haskell.tar.gz
    sudo ./install-haskell-platform.sh

If you are on x64:

    wget https://haskell.org/platform/download/8.0.1/haskell-platform-8.0.1-unknown-posix--full-x86_64.tar.gz -O /tmp/haskell.tar.gz
    cd /tmp
    tar xvzf /tmp/haskell.tar.gz
    sudo ./install-haskell-platform.sh

Then restart your shell. Check that you have the correct version
(8.0.1) by running:

    ghc --version
    The Glorious Glasgow Haskell Compilation System, version 8.0.1

If you do not, you probably already had a version of the haskell
platform installed. Uninstall that and you will be good to go.

The above is just a copy-paste-able format of
the instructions in
[haskell.org](https://www.haskell.org/platform/linux.html#linux-generic)
