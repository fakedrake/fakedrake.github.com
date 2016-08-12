title: Intstalling NVM and node-js on unix
date: 2016-08-12 11:51
tags: nodejs
category: unix
slug: intstalling-nvm-and-nodejs
author: Chris Perivolaropoulos

Just run the following that will setup everything for you:

    wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.31.4/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" # This loads nvm
    nvm install node
    nvm use node

This will run everything for you. Check the version:

    $ node --version
    v6.3.1

Your version may differ. This is a concise version of the
[official instructions](https://github.com/creationix/nvm#install-script)
