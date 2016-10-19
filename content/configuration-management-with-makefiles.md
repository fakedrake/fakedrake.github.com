title: Configuration management with makefiles
date: 2015-05-15 13:58
tags:
category:
slug: configuration-management-with-makefiles
author: Chris Perivolaropoulos
status: draft
summary: Dependency graph made that with arbitrary commands.

_This article is hidden. Remove status: hidden or make it status:
published to be able to publish_

All the cool kids now use configuration managers like chef and
ansible. Those are pretty cool for most dev ops jobs but I have found
myself to be working against them rather than them helping me automate
everyday stuff. So I prefer makefiles whenever I can. For other
dependency management tools having tasks depend on the success or fail
of a command rather than the existence of a file is trivial but here
is a way to do it pretty easily with makefiles.

Consider the following case, we have two repositories RepoA and
RepoB. RepoB needs to know the most recent version of RepoA that we
are developing so whenever we make a release we need to make a pull
request for RepoB that is based on it's branch development. This task
can be tedious and things can go wrong. Let's automate the whole
process.

Make the two repositories:

    mkdir /tmp/RepoA
    mkdir /tmp/RepoB

    cd /tmp/RepoA
    echo "version: 0.1" > manifest
    git init
    git add manifest
    git commit -a -m "Initial commit"

    cd /tmo/RepoB
    echo "version: 0.1"
    echo "dependencies:"
    echo "\tRepoA: 0.0.1" > manifest
    git init
    git add manifest
    git commit -a -m "Initial commit"
    git checkout -b development
    echo "\totherDep: 1.0" >> manifest
    git commit -a -m "Extra dependencies"
    git checkout master

So now we have two repos with only manifest files and RepoB has a
development branch.

The cool part of Makefiles is that variables are constructed lazily
and recursively. Let's abuse that to switch to development if we are
not there and do nothing if we are not. Let's make some boilerplate

    dep-ok:
        touch dep-ok

    new-command-dep=$(shell ($1) > /dev/null && echo dep-ok || echo
    $2)

This make function will help us give two kinds of information

- The command that we need to make succeed
- A target that when run will actually do the work

Here we will use it for our example

    bgit=git -C /tmp/RepoB
    b-on-branch=$(call new-command-dep,$(bgit) branch|grep -F "* $1",b-on-branch-$1)
    b-on-branch-%:
        $(bgit) checkout $*

Now we can run

    make b-on-branch-master

And it will switch to master if we are not on master, or do nothing
(run target `dep-ok`) if we already are..
