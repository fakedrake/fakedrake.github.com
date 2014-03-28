title: When printks are too many
date: 2014-03-28 20:45
tags: git, kernel, debugging
category: kernel
slug: when-printks-are-too-many
author: Chris Perivolaropoulos
summary: Clean your code from your extra printks with git.

As I am too lazy to be using proper debugging methods (although what
proper debugging methods can be
[debateable](http://www.linuxtoday.com/infrastructure/2000090700221OSCYKN))
I always (over)use printks to debug the kernel. Now the problem with
printks is that when you find your bug they are all over the kernel
code and it can be a real pain to remove them one by one.

This is not a trivial problem when you spend more than a couple of
hours on a particular problem. The good news is that due to the nature
of printk-debugging you usually know which one of your nasty hacks
fixed the problem you were looking for. Thus you can `git diff` those
to just keep the useful changes (I use emacs' ediff, meld or anything
interactive should be good enough), then you commit just those.

You should learn from my mistakes and not blindly `git checkout` at
the project root. For me there are usually some nasty device tree
changes that I make to fit Qemu and also my .config is setup for
debugging. I definitely dont want reverting any of that. Actually all
I want to revert is the .c files I threw printks in.

	git status | sed -n 's/.*modified: *\(.*\.c\)/\1/p' | xargs git checkout

Works 99% of the time. To avoid the tragedy of the other 1% make sure
you take a look at `git status` _beforehand_.
