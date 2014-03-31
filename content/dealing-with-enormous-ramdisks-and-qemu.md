title: Dealing with enormous ramdisks and Qemu
date: 2014-03-31 22:30
tags: kernel, qemu
category: kernel
slug: dealing-with-enormous-ramdisks-and-qemu
author: Chris Perivolaropoulos
summary: There are times when you want to have everything on RAM. There are times when everything is more than 500M. And then there are times when you want both. That's when everything goes to hell.

*DISCLAIMER:* This is hacky and BAD. Do not use 500M ramdisks for
 anything crucial. Make them small and mount the rest of the
 filesystem in `rootfs=<fs>` in boot commands and the `-hda` option on
 qemu or use nfs or whatever.

So there are times in Think-Silicon land when permanent storage
devices may not always be there for you. May that be because your
ethernet device screws up and you are relying on NFS for fsroot, or
may it be because I just want the kernel to do my bidding and load a
ramdisk that is as big as half a Gigabyte. The point is shoving such a
big ramdisk down the kernel's throat will result in it choking into
something like this:

	...

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

Let's start at the beginning. When the kernel registers a block device
it then registers a number of disks with the same major number that
take upon them the actual work. To those disks is mapped the actual
memory. This paradigm is implemented in _block/genhd.c_. This
description is also neither complete nor 100% accurate but it is
enough for now.

When the kernel boots up, one of the first drivers it loads is one
called _brd_ as in _block ramdisk device_. That driver creates a block
device interface to the main memory and lives in
_drivers/block/brd.c_. The block device _ramdisk_ with major number 1
is created and gets disks called _ram#_ as in _ram0_, _ram1_,
..., 16 by default. Those disks each represent a space in virtual memory and have the
same size which by default is 16M. The problem we faced above is
basically the kernel trying to fit a 500M initrd in a 16M disk. What
we need to do basically is resize those so that the ramdisk fits
nicely.

As either google or the code in _brd.c_ will kindly tell you you can
always tell the kernel in the boot commands
_ramdisk\_size=500000_. That will supposedly set thing up so that we
can just tell qemu `-initrd <fucking-huge-ramdisk.img>` right?!?

![Check yo shit](http://www.themistermen.co.uk/images/MrWrong.jpg)

WRONG!!

The kernel tries to create 16 such 500M disks. Which sucks. We need to
change the number of disks the driver creates. You can do that via the
`CONFIG_BLK_DEV_RAM_COUNT` option but I hate having to compile the
entire kernel to change something that can to some extent be changed
from user space. Did I mention you can create more disks with `rdev
-r` from the shell? That is because I have no idea if it is
true. _Documentation/blockdev/ramdisk.txt_ betrayed me once with
mentioning that I can `ramdisk_blocksize=N` which if you grep the
source is hard to believe, and trust is lost easier than earned.

Anyway what I ended up doing is editing `ramdisk_size()` from this

	:::c
	/* Legacy boot options - nonmodular */
	static int __init ramdisk_size(char *str)
	{
		rd_size = simple_strtol(str, NULL, 0);
		return 1;
	}

to look more like this

	:::c
    /* Legacy boot options - nonmodular */
    static int __init ramdisk_size(char *str)
    {
    	int tmp, index = 0;

    	while (get_option(&str, &tmp)) {
    		switch (index++) {
    		case 0:
    			rd_size = tmp;
    			break;
    		case 1:
    			rd_nr = tmp;
    			break;
    		}
    	}

    	return 1;
    }

Now you can pass _ramdisk\_size=500000,1_ to tell the driver to make
just one 500M disk, while having _ramdisk\_size=500000_ behave as
before. Noice!

So now we simply run qemu

	qemu-system-arm -M xilinx-zynq-a9 -m 1024 -serial null -serial
		mon:stdio -dtb ./devtree.dtb -kernel path/to/zImage
		-initrd path/to/enormous-ramdisk.img -nographic
		-append "console=ttyPS0,115200 root=/dev/ram rw ip=:::::eth0:dhcp \
			loglevel=7 ramdisk_size=500496,1p"

And everything boots correctly!!

I always run qemu from within a script so for completeness here is the
relevan excerpt

	:::bash
	...

	BOOTCMD="console=ttyPS0,115200 root=/dev/ram rw ip=:::::eth0:dhcp loglevel=7 ramdisk_size=$(du --apparent-size $RAMDISK | awk '{print $1}'),1p'"
	CMD="$QEMU -M xilinx-zynq-a9  -m 1024  -serial null -serial mon:stdio -dtb $DTB -kernel $KERNEL -initrd $RAMDISK -nographic"

	echo -e "Running: $CMD -append $BOOTCMD\nC-a x to kill..."
	$CMD -append "$BOOTCMD"

As an extra benefit this will actually measure the ramdisk and make
the disk size only as big as it needs to be.
