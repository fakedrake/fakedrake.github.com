title: Subclassing function types in python
date: 2016-09-18 11:59
tags: python
category: python
slug: subclassing-function-types
author: Chris Perivolaropoulos
summary: The way callables work in python can be a bit strange.  You have methods that take an argument `self` but only when called from an object and classmethods and static methods etc. Let's take a more in-depth look at how cpython handles all this

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

`typenames` is now a function that will evaluate to a list of names of
the types of the instance we give it. Let's check that it works

    >>> typenames(1)
    ['IntType']
    >>> typenames('1')
    ['StringType']
    >>> typenames(True)
    ['BooleanType']

Let's take a look at the types of different built in callable types:

    >>> typenames(func)
    ['LambdaType', 'FunctionType']
    >>> typenames(labd)
    ['LambdaType', 'FunctionType']
    >>> # Ordinary methods
    >>> typenames(A.method)
    ['UnboundMethodType', 'MethodType']
    >>> typenames(A().method)
    ['UnboundMethodType', 'MethodType']
    >>> # Static methods
    >>> typenames(A().stemeth)
    ['LambdaType', 'FunctionType']
    >>> typenames(A.stemeth)
    >>>
    ['LambdaType', 'FunctionType']
    >>> typenames(A.clsmeth)
    ['UnboundMethodType', 'MethodType']
    >>> typenames(A().clsmeth)
    ['UnboundMethodType', 'MethodType']

So there are (at least) four built in callable types.

- `FunctionType`
- `LambdaType`
- `UnboundMethodType`
- `MethodType`

Calling them we can see the various:

    >>> A.stemeth()
    >>> A().stemeth()
    >>> A.clsmeth()
    (<class '__main__.A'>,)
    >>> A().clsmeth()
    (<class '__main__.A'>,)
    >>> A.method()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unbound method method() must be called with A instance as first argument (got nothing instead)
    >>> A().method()
    >>>

Note:
[types.py](https://github.com/python/cpython/blob/master/Lib/types.py)
does pretty much the same thing to get hold of the types themselves
but for educational reasons let's pretend that what we just did is not
stupid.
