title: Functional programming
date: 2015-09-12 19:03
tags:
category:
slug: functional-programming
author: Chris Perivolaropoulos
status: draft
summary:

_This article is hidden. Remove status: hidden or make it status:
published to be able to publish_

Types are a weird scheme that is faced differently from different
languages. There are 3 main viewpoints that languages have on them:

- The C/C++/Java approach: Types will make it easier for the compiler
  to make code more efficient. They will also force the programmer to
  write code that is more friendly to the the compiler itself.
- The dynamic type approach: Languages like Javascript, python, Ruby
  and most lisps put having a flat learning curve first, at times at
  the cost of. They move the burden of managing types completely on
  the side of the runtime.
- The more hardcore functional languages like haskell and ML use types
  to try to assert the correctness of a program at compile time, to
  (at least partially) document code but most importantly to infer as
  much logic as possible.

The main "trick" that is employed for this is Monads. They say that once
you grasp what a monad is you lose the ability to explain what a monad
is. The fact that you could not explain them in the first place either
aside, this slightly delayed article is a continuation of the
tradition of programmers who grasp the concept, to miserably fail to
disseminate their epiphany.

# Monads

There are many analogies for what a monad is out there. Most commonly
it is compared to a box, a burrito, or a line of elephants. Those all
served much more to confuse me than help me understand. After much
meditation on the subject and many pages of mathematical
interpretations it finally dawned on me while I was reading
[this](http://www.cs.ioc.ee/tfp-icfp-gpce05/tfp-proc/03num.pdf) paper
on comonads. So like Aristotle let's start at the end.

Say you have a type T (eg the set of real numbers) and you have many
tools in your arsenal with dealing with it, slicing it, combining it,
tranforming it and what have you. *An instance of a monad over T is
something that you can treat like a T but is not a T.* You also have
the means of creating instances of M T and creating M T values from T
values but no way of making use these M Ts. You can however draw
direct parallels of how to manipulate M T based on how you can
manipulate T. To also be formal:

    class Monad m where
      return :: a -> m a
      (>>=) :: m a -> (a -> m b) -> m b

A usecase is that we can easily plumb together functions that from a
value can produce a sort-of-value. Eg if we can send to a device a
message and get a promise of a message (sort-of-a-message, it's a
message but we don't have it yet). With the framework of monads we can
easily chain these together. In essence we use the IO monad (the sort
of message) as if it were a message.

It is obvious I believe that the notion of a functor is shaping out
very obviously from the above. Indeed a monad is also a functor, but
there is an intermediate state.

# Functors

We can view functions like maps from each element of one set to an
element of another set. That is sort of like transforming a set of
elements into another set of elements. A functor takes that two steps
further. From a set of sets it can tranform each one into a new
set. Furthermore if a a set of the original bag was a transformation
from another set in that bag the functor can trasform that
trasformation too! (inception).

To put it another way a functor can transform a category into another
category. More formally

    class Functor f where
        fmap :: (a -> b) -> f a -> f b

An infix version of `fmap` is `<$>`. This will come up in the next
section.

# Applicative

Applicative functors are the part of a monad that allows it to be used
just like the underlying type.

    class (Functor f) => Applicative f where
        pure  :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b

I suggest you go over the
[wikibok on applicatives](https://en.wikibooks.org/wiki/Haskell/Applicative_functors). To
provide a gist for this, all monads need to be applicatives and
therefore implement this interface. `pure` is the same as `return` so
ok. Notice how `<*>` is a bit like fmap only for wrapped
functions.

As a practical rule to memorize about applicatives, when you fmap to a
function that takes more than one arguments to an argument you get a
wrapped function. Applicatives are then the right tool. Use `<*>` make
the wrapped function into a wrapped value.

For example

    Prelude> :t (+) -- Takes two arguments
    (+) -- Takes two arguments :: Num a => a -> a -> a

    Prelude> :t fmap (+) (Just 1)  -- Curry it to one, but now it's wrapped
    fmap (+) (Just 1)  -- Curry it to one, but now it's wrapped
      :: Num a => Maybe (a -> a)

    Prelude> :t (fmap (+) (Just 1)) <*> Just 2  -- Thankfully Maybe is an applicative and supports <*>
    (fmap (+) (Just 1)) <*> Just 2  -- Thankfully Maybe is an applicative and supports <*>
      :: Num b => Maybe b

    Prelude> (fmap (+) (Just 1)) <*> Just 2  -- Thankfully Maybe is an applicative and supports <*>
    Just 3


# Monoids


*TODO*

# CoMonads

Comonads are the reverse of monads. They are things that you know how
to manipulate, but you can not really create very easily, or at
all. This sounds a bit strange but bare with me.

Comonads can be used for computations that require an implicit context,
ie dataflows. A comonad in this case is a value along with some sort of
context.

cobind :: (CA -> B )-> (CA -> CB) is to say that given a function that
maps a value along with some context to another value is we can create
a function that will map the same thing to the other value plus
context. In other words we can map a stream of As to a stream of Bs if
we can map a stream of As to a B. This means that we can pipe stream
functions together that do not use the same context. To generalize
that, if we have functions that map contexts of planes to points in
other planes we can trivially pipe those together.

Here we have the means to create the underlying type but for the
specific use we are better at manipulating the Comonad than
manipulating the underlying type.
)
