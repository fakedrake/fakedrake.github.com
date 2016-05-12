title: Multi-argument function composition
date: 2016-04-01 12:05
tags: haskell
category:
status: draft
slug: multiple-argument-function-composition
author: Chris Perivolaropoulos
summary:Multiple argument function composition

Function composition is what functional programming is about. In
haskell composition in general is the main theme. Function composition
is in theory easy:

    Prelude> let f = (+1)
    Prelude> :t f
    f :: Num a => a -> a
    Prelude> let g = (+2)
    Prelude> :t g
    g :: Num a => a -> a

So `f` and `g` are composed with the `(.)` operator to make a new
function `f ( g (x) )`.

    Prelude> :t f.g
    f.g :: Num c => c -> c
    Prelude> (f.g) 1
    4

Which is simple. Enter a new function `h`.

    Prelude> let h = (-)
    Prelude> :t h
    h :: Num a => a -> a -> a

How would we compose `f` and `h` so that we get `l(x,y) = f(h(x,
y))`. We will use the operator `((.).(.))`.

    Prelude> let (<.>) = ((.).(.))
    Prelude> :t f <.> h
    f <.> h :: Num c => c -> c -> c
    Prelude> (f <.> h) 1 2
    0
    Prelude> (f <.> h) 1 3
    -1

So now that we have the final answer let's talk a bit about what just
happened. Let's look at what happens on a lambda calculus level.
