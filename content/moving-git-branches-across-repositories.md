title: Moving git branches across repositories
date: 2014-05-07 15:49
tags: git, branch, shell
category: git
slug: moving-git-branches-across-repositories
author: Chris Perivolaropoulos
summary: When cloning seems to be the only option for moving to a new remote repo of your project, you probably aren't willing to copy your work so far by hand. Especially when git can do it for you.

In a perfect world there is a one-to-one relationship between projects
and git trees. As you are happily working on your local repo, and
decide you want to get some commits from a different source you just
`git remote add` that source and you have full access to it's
commits. Well sometimes things do not go as smoothly and you may find
yourself wanting to move your branch to a remote repo that may have a
largely common codebase but few to no common commits. Well turns out
git can handle that pretty easily. Here is how in one line:


	:::console
	git log --reverse --cherry master...<your-branch> --pretty=email --patch-with-stat | (cd /path/to/new/repo && git checkout -b <your-branch> && git am)


It is quite simple really: we use `git log` to get a comprehensive
description of each commit in `<your-branch>`. Then create a new
branch at the new repo with the same name and pipe the descriptions of
the commits to `git am` to create them in the new place.

*Note:* the commits in the new repo will not have the same SHA as in
 the old one so we are not really _moving_ the commits from one repo
 to another as much as _recreating_ them.
