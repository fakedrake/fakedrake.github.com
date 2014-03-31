title: Dealing with enormous ramdisks and Qemu
date: 2014-03-31 22:30
tags: kernel, qemu
category: kernel
slug: dealing-with-enormous-ramdisks-and-qemu
author: Chris Perivolaropoulos
summary: There are times when you want to have everything on RAM. There are times when everything is more than 500M. And then there are times when you want both. That's when everything goes to hell.

So there are times in Think-Silicon land when permanent storage
devices may not always be there for you. May that be because your
ethernet device screws up and you are relying on NFS for fsroot, or
may it be because I just want the kernel to do my bidding and load a
ramdisk that is as big as half a Gigabyte. The point is shoving such a
big ramdisk down the kernel's throat will result in it choking into
something like this:

	RAMDISK: ext2 filesystem found at block 0
	RAMDISK: image too big! (500496KiB/16384KiB)
	xemacps e000b000.eth: Set clk to 124999998 Hz
	xemacps e000b000.eth: link up (1000/FULL)
	List of all partitions:
	1f00            1024 mtdblock0  (driver?)
	1f01            5120 mtdblock1  (driver?)
	1f02             128 mtdblock2  (driver?)
	1f03            6016 mtdblock3  (driver?)
	1f04            4096 mtdblock4  (driver?)
	No filesystem could mount root, tried:  ext3 ext2 ext4 vfat msdos
	Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(1,0)

Turns out you can do something about it, may it be hacky and
horrible. This is the tale of a glorious journey through the mysts of
the linux kernel to a busybox prompt inside of Qemu.

# Down the rabbit hole

So going down the rabbit hole that is the linux kernel our first stop
is the spot where that `image too big!` shows up.
