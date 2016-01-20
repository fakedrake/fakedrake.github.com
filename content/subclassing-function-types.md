title: Subclassing function types
date: 2015-09-18 11:59
tags:
category:
slug: subclassing-function-types
author: Chris Perivolaropoulos
status: draft
summary:

_This article is hidden. Remove status: hidden or make it status:
published to be able to publish_

Disclaimer: The following is based on cpython.

    >>> class A(object):
    ...     @classmethod
    ...     def clsmeth(cls): pass
    ...     @staticmethod
    ...     def stemeth(): pass
    ...     def method(self): pass
    ...
    >>> def func(): pass
    ...
    >>> labd = lambda x: x

And let's define a way of finding out the corresponding type in the
types module

    >>> import types
    >>> typenames = lambda inst: [n for n,t in types.__dict__.items() if t is type(inst)]

Let's check that it works

    >>> typenames(1)
    ['IntType']
    >>> typenames('1')
    ['StringType']
    >>> typenames(True)
    ['BooleanType']

Let's take a look at the callable types we just defined:



Note:
[types.py](https://github.com/python/cpython/blob/master/Lib/types.py)
does pretty much the same thing to get hold of the types themselves
but for educational reasons let's pretend that what we just did is not
stupid.
