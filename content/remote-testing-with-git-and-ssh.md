title: Remote testing with git and ssh
date: 2014-05-11 21:37
tags: testin, git, ssh, remote
category: git
slug: remote-testing-with-git-and-ssh
author: Chris Perivolaropoulos
status: draft
summary:

_This article is hidden. Remove status: hidden or make it status:
published to be able to publish_

Running tests is an important part of the development workflow. You
want to do it often and yo want it to be quick. Sometimes tests are
not quick. Depending on what you are building tests can be slow and
memory intensive. This means that you probably prefer to run them on a
powerful server rather than your slow, low memory laptop that you like
using by on the beach away from power outlets. "You know what would be
awesome?" I thought to myself while sipping pina collada on the roof
garden of Think Silicon HQ, "if I could push my changes to a remote
server with git, run the test with ssh and get the results with just
one command!".

So I made a branch I call `bench` because I was running some
benchamrks at the time and pushed it to github. Then I pulled the
branch from our awesome server and ran the tests. They finished in a
fourth of the original time and my workstation was fully function
during the whole time! "Nice" I thought to myself. Then I got the
results parsed in emacs' compilation mode and tried to jump to the
first error which of course failed due to the difference absolute
paths. One way would be to convert all paths to relative but it would
prefer absolute paths to work as well so I decided i would pipe the
output through sed. Anyway I came up with *remote_test.sh*:

	:::sh
	#!/bin/sh

	REMOTE_ROOT="/path/to/remote-test"
	LOCAL_ROOT="/path/to/test"

	REMOTE_SRV=localhost # for testing
	REMOTE_USER=`whoami`

	SED_REMOTE_ROOT=$(echo $REMOTE_ROOT | sed 's/[\/&]/\\&/g')
	SED_LOCAL_ROOT=$(echo $LOCAL_ROOT | sed 's/[\/&]/\\&/g')

	function local_paths {
		sed "s/$SED_REMOTE_ROOT/$SED_LOCAL_ROOT/g"
	}

	function remote_paths {
		sed "s/$SED_LOCAL_ROOT/$SED_REMOTE_ROOT/g"
	}

	ARGS="$@"
	REMOTE_CMD=$(echo $ARGS | remote_paths )
	REMOTE_PWD=$(pwd | remote_paths )

	echo Running: $REMOTE_CMD

	ssh $REMOTE_USER@$REMOTE_SRV "cd $REMOTE_PWD && $REMOTE_CMD" |& local_paths


Notice the escaping of the paths so that characters in the paths dong
get confused for parts of the sed command. So let's test it.

Run the tests again like this now:

	:::console
	$./remote_test.sh echo Path is: /path/to/test >&2'
	Running: echo Path is: /path/to/remote-test
	fakedrake@localhost's password:
	Path is: /path/to/test

Notice how the path on the command run by the remote server makes
sense to the server and the standard error when returned to us makes
sense to the local workstation. Thus if you like me have some
interesting way to generate paths in your test commands (ie some emacs
lisp to create run tests on a project local python virtual env) they
will be translated to paths that make sense on the server.

That is awesome but unless you use NFS (or afs or whatever) for home
directories like we do in Think Silicon you also need to let the
server know what changes you made in the code. That is why we have
git. My approach to solving this is to have a temporary branch (ie
`bench`) that I will commit to whenever I want to run a test. Then
that branch will be pushed to the server and the tests will run with
the most recent code.

However it is not very straightforward to just push changes to a
remote working tree and I would hate to get into port forwarding on my
local net if I am working from home so here is a hacky workaround for
this. Make a bare repository local to the server where I can push
commits from `bench`. Once those are pushed, and before running the
tests on remote, the server will pull those changes, which should be
pretty fast since the repo is in the same filesystem.

So on the server do

	:::console
	$ cd ~
	$ mkdir .testing
	$ cd .testing
	$ git clone --bare <some mirror of the project>
	$ cd /path/to/remote/project
	$ git remote add testing $HOME/.testing/project.git
	$ git checkout bench

On the local workstation add this remote:

	:::console
	$ cd /path/to/local/project
	$ git remote add testing /home/remote-user/.testing/project.git

Then in make *test_remote.sh* push there before doing anything else:

	:::sh
	BRANCH=$(git branch | awk '/\*/{print $2}')
	GIT_REMOTE=local

	function git_draft_sync {
		COMMIT_MSG="[$(date +%s)] Draft commit"

		echo "Will now commit a dumb commit to current branch."

		echo Commiting: $COMMIT_MSG
		git commit -a -m "$COMMIT_MSG"

		echo Pushing branch: $BRANCH
		git push $GIT_REMOTE $BRANCH
	}

And the remote command should now be

	:::sh
	REMOTE_CMD="(git pull testing $BRANCH && $(echo $ARGS | remote_paths))"

and dont forget to run `git_draft_sync`.

Thus my real world script for running python tests on a remote server
at CSAIL

	:::sh
	#!/bin/sh

	# Paths (don't use / at the end)
	REMOTE_ROOT="/path/to/remote/home/Projects"
	LOCAL_ROOT="/home/fakedrake/Projects/CSAIL/Python"
	REMOTE_SRV=<remote-server>
	REMOTE_USER=<username>


	BRANCH=$(git branch | awk '/\*/{print $2}')
	GIT_REMOTE=local

	function git_draft_sync {
		COMMIT_MSG="[$(date +%s)] Draft commit"

		echo "Will now commit a dumb commit to current branch."

		echo Commiting: $COMMIT_MSG
		git commit -a -m "$COMMIT_MSG"

		echo Pushing branch: $BRANCH
		git push $GIT_REMOTE $BRANCH
	}

	## -- No need to edit from here on --
	SED_REMOTE_ROOT=$(echo $REMOTE_ROOT | sed 's/[\/&]/\\&/g')
	SED_LOCAL_ROOT=$(echo $LOCAL_ROOT | sed 's/[\/&]/\\&/g')

	function local_paths {
		sed "s/$SED_REMOTE_ROOT/$SED_LOCAL_ROOT/g"
	}

	function remote_paths {
		sed "s/$SED_LOCAL_ROOT/$SED_REMOTE_ROOT/g"
	}

	ARGS="$@"
	REMOTE_CMD="(git pull testing $BRANCH && $(echo $ARGS | remote_paths ))"
	REMOTE_PWD=$(pwd | remote_paths )

	echo "Running perliminaries:"

	echo ARGS: $ARGS
	echo Running: $REMOTE_CMD
	echo Directory: $REMOTE_PWD
	echo At: $REMOTE_USER@$REMOTE_SRV

	git_draft_sync
	ssh $REMOTE_USER@$REMOTE_SRV "cd $REMOTE_PWD && $REMOTE_CMD" |& local_paths

Put this in the root directory of your project and change the paths at
the top of the script to something that makes sense for you. Then tell
your editor or whatever to prepend `./remote_test.sh` before the test
command. thus emacs will do:

	-*- mode: compilation; default-directory: "~/Projects/CSAIL/Python/WikipediaBase/" -*-
	Comint started at Sun May 11 23:17:22

	./remote_test.sh /home/fakedrake/Projects/CSAIL/Python/py//bin/python  setup.py test
	Running perliminaries:
	ARGS: /home/fakedrake/Projects/CSAIL/Python/py//bin/python setup.py test
	Running: (git pull testing bench && /path/to/remote/home/Projects/py//bin/python setup.py test)
	Directory: /path/to/remote/home/Projects/WikipediaBase
	At: <user name>@<remote-server>
	Will now commit a dumb commit to current branch.
	Commiting: [1399839442] Draft commit
	On branch bench
	Untracked files:
		TAGS
		[...]

	nothing added to commit but untracked files present
	Pushing branch: bench
	Password:
	Everything up-to-date
	Password:
	From /path/to/remote/home/.testing/WikipediaBase
	 * branch            bench      -> FETCH_HEAD
	Already up-to-date.
	running test
	running egg_info

	[...]

And compilation-mode sees the paths that it expects so I can jump
around the source based on the errors.
