title: Enabling python virtualenvs dumb and fast
date: 2014-07-16 19:27
tags: python, virtualenv, shell
category: python
slug: enabling-python-virtualenvs-dumb-and-fast
author: Chris Perivolaropoulos
summary: Enable the right virtualenv without really thinking about it or over-engineering.

Unless you are using
[virtualenvwrapper](https://bitbucket.org/dhellmann/virtualenvwrapper/)
or something else fancy that the cool kids like these days a common
series of commands to run python tests is. I also annotated my
thinking process for dramatic purposes.

	:::console
	# Let's work on awesome-project a bit
	$ cd python/project/path/awesome-project
	# That went well, good job, you deserve eternal love and
    # admiration, running some tes- crap, I need the virtualenv...
	$ ls ..
	# Pff ok which one of those looks like a virtualenv...
	$ . ../py/bin/activate
	# Bingo! Where was I?
	$ python setup.py test

Now besides being lazy I am also inconsistent, dumb and have a very
hard time context switching like that. Thankfully shell scripting can
help out with this. I recently added this stupid little function in my
_.zshrc_ and my life has been a wonderful journey in unicorn rainbow
land ever since

	:::shell
	# find the first venv backwards and activate it.
	pv() {
		A=./*/bin/activate;
		for i in {1..$(pwd | grep -o / | wc -l)}; do
		if bash -c "ls $A" 2> /dev/null; then
			source $(bash -c "ls $A | head -1");
			break;
		fi;
		A=../$A;
		done
	}

Now it's all like

	:::console
	# Work on awesome-project
	$ cd python/project/path/awesome-project
	# Women and glory are just around the corner, Oh, virtualenv
	$ pv
	# Set!
	$ python setup.py test
	[...]
