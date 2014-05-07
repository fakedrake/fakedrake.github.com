title: Gdb signals
date: 2014-05-06 16:36
tags: GDB, C/C++, signals
category: GDB
slug: gdb-signals
author: Chris Perivolaropoulos
summary: Signaling from and to a process through GDB is much easier than one might expect.

So unless you are debugging your own program and you know what you are
doing this is probably not what you expect to happen while a program
runs under GDB.

	Program received signal SIGUSR1, User defined signal 1.
	[Switching to Thread 0x7fffcff2c700 (LWP 3296)]
	...
	(gdb)

You may hit `c` to continue but this will come up again sooner or
later and I like my breakpoints to be tidy.

First take a look at how gdb handles each signal.

<div class="highlight"><pre>
(gdb) info signals
Signal        Stop	Print	Pass to program	Description

SIGHUP        Yes	Yes		Yes		Hangup
SIGINT        Yes	Yes		No		Interrupt
SIGQUIT       Yes	Yes		Yes		Quit
SIGILL        Yes	Yes		Yes		Illegal instruction
SIGTRAP       Yes	Yes		No		Trace/breakpoint trap
SIGABRT       Yes	Yes		Yes		Aborted
SIGEMT        Yes	Yes		Yes		Emulation trap

[...]

SIGWINCH      No	No		Yes		Window size changed
SIGLOST       Yes	Yes		Yes		Resource lost
<b>SIGUSR1	    Yes	Yes		Yes		User defined signal 1</b>
SIGUSR2       Yes	Yes		Yes		User defined signal 2
SIGPWR        Yes	Yes		Yes		Power fail/restart

[...]

EXC_EMULATION Yes	Yes		Yes		Emulation instruction
EXC_SOFTWARE  Yes	Yes		Yes		Software generated exception
EXC_BREAKPOINT Yes	Yes		Yes		Breakpoint

Use the "handle" command to change these tables.
</pre></div>

As the command says you want `SIGUSR1` to not stop and also for it to
be passed to the program. The other thing we notice here is that
`SIGTRAP` is not passed to the program.

To have `SIGUSR1` be ignored by GDB

	(gdb) handle SIGUSR1 nostop noprint
	Signal        Stop	Print	Pass to program	Description
	SIGUSR1       No	No	Yes		User defined signal 1

Now here is another recurring interrupt related issue: Sometimes you
need to to pass control to gdb while the program is running. The
default way would be to hit `C-c`. In a very rare occasion (ie. qemu)
the process will catch the key and will not stop. Instead of
despairing you can try sending it a `SIGTRAP`. That will stop the
program as if gdb had encountered a breakpoint. From another terminal
run.

	:::console
	$ pkill -TRAP <process-name>

If you are using _emacs_ and _gud_ like me you can automate this with:

	:::lisp
	(defun my:gud-trap-process (&optional wrapping-script)
	  (interactive "*P")
	  (let ((child-pid "xargs pgrep -P | head -1 |"))
		(async-shell-command
		 (format "echo %d | %s %s xargs echo kill -TRAP"
			 (process-id (get-buffer-process "*gud*"))
			 child-pid (if wrapping-script child-pid "")))))

Putting this in your _.emacs_ will let you do `M-x
my:gud-trap-process` to give control to gdb. If you are running gdb
from within a shell script like I usually do provide a prefix
argument, ie. `C-u M-x my:gud-trap-process` to handle child processes
correctly. I also have it bound to `C-x C-a t` for brevity:

	(global-set-key (kbd "C-x C-a t") `my:gud-trap-process)

This process will not run exactly the shell command I mentioned
earlier but rather it will find the pid of gdb and send `SIGTRAP` to it's
first child process. So if you want to automate the process in another
way here is the main idea:

	$ pgrep -P <gdb pid> | head -1 | xargs kill -TRAP
