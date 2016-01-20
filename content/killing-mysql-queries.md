title: Killing mysql queries
date: 2016-01-20 13:07
tags:
category:
slug: killing-mysql-queries
author: Chris Perivolaropoulos
summary: Killing long jobs for mysql

MySQL queries are many times painfully slow. So slow that it is not
worth waiting. Here is how to kill a running query.

First of all you need to know what is running to choose what to kill.

    > show processlist
    |       Id | User | Host | db      | Command | Time | State        | Info                      |
    |----------+------+------+---------+---------+------+--------------+---------------------------|
    | 35162105 | me   | host | db_name | Query   |  183 | Sending data | SELECT * FROM `HugeTable` |
    | 35162616 | me   | host | db_name | Query   |    0 | NULL         | show processlist          |
    | 35162617 | me   | host | db_name | Sleep   |    0 |              | NULL                      |

The last process we don't care about and the one before that is the
one we just ran to get the process list itself. The first one is the
one to kill. So now that we have the id, we can kill it by running

    > kill 35162105

And we freed up the server!
