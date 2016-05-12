title: Limiting simultaneous threads in Haskell
date: 2016-04-29 02:23
tags:
category:
slug: limiting-parallel-thread-in-haskell
author: Chris Perivolaropoulos
summary: A simple way to lock the number of parallel threads with MVar.

Iwas making a mini crawler to download all mp3s from a website in
Haskell and was confronted with the following problem: it is easy to
download stuff serially or to download them all in parallel. What is
slightly harder is to download just a couple in parallel.

I will start with an introduction it `MVar`. Let's say we want a
safer `putStrLn` that does not interleave it's output with other
`putStrLn`s but rather waits for it's turn:

``` haskell
import Control.Concurrent.MVar

putStrLn' lock x = do
  putMVar lock ()
  putStrLn x
  takeMVar lock
```

Then we call it like this:

``` haskel
main = do
  ioLock <- newEmptyMVar
  ...
  putStrLn' ioLock $ "Found talks: " ++ (show $ length urls)
```

Now that was fairly easy. What about the case where we want a few
simultaneous threads and the rest should wait for any of them to
finish.

``` haskell

-- | There is no 0 state for MVar. 0 means taken. So check if it is
-- taken and if so treat it as 0 by putting 1, otherwise take,
-- increment, put
increment :: MVar Int -> IO Int
increment procs = do
  taken <- isEmptyMVar procs
  if taken then putMVar procs 1 >> return 1 else do
    num <- takeMVar procs
    putMVar procs (num +1)
    return (num+1)

-- | If we are going for 0 don't put back. 0 is special in that it
-- blocks everyone trying to decrement.
decrement :: MVar Int -> IO Int
decrement procsLock = do
  num <- takeMVar procsLock
  if num > 1 then putMVar procsLock (num-1) >> return (num-1) else return 0

-- | Decrement until we are done then increment
guarded :: MVar () -> MVar Int -> IO a -> IO a
guarded ioLock procsLock io = do
  slotsLeft <- decrement procsLock
  putStrLn' ioLock ("Slots left: " ++ show slotsLeft)
  ret <- io
  increment procsLock
  return ret
```

You can call it like this:

``` haskell
import Control.Monad.Parallel

main = do
  procs <- newMVar 5
  ...
  data_ <- mapM_ (guarded ioLock procs . getUrl ioLock) urls
```

And `getUrl` will run at most 5 times simultaneously.
