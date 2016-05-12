title: Streaming Data through HTTP with Haskell
date: 2016-04-30 03:33
tags:
category:
slug: streaming-data-through-http-with-haskell
author: Chris Perivolaropoulos
summary: Download and process large files on the fly with haskell

So I wanted to do some processing on wikipedia articles but I don't
have enough disk space to download them first and process them later,
it needs to be on-the-fly. Fortunately they are stored bziped which
means they are compressed at the block level and I don't need the last
byte to know what the first one means. So I begun by finding a way to
stream data. I struggled with Conduit a bit but then I stumbled upon a
much simpler solution:

``` haskell
import Network.HTTP.Client
import Network.HTTP.Client.TLS   (tlsManagerSettings)
import Control.Monad.Fix
import Data.Conduit
import qualified Data.ByteString as BS

url = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"

printLen bytes = putStrLn $ "Got bytes: " ++ (show $ BS.length bytes)

getResp :: String ->  IO ()
getResp url = do
  man <- newManager tlsManagerSettings
  req <- parseUrl url
  withResponse req man $ \res -> do
    putStrLn "Got a response, now streaming..."
    fix $ \loop -> do
      bytes <- brRead $ responseBody res
      if BS.null bytes then putStrLn "Done!" else do
        putStrLn $ "Got " ++ show (BS.length bytes) ++ " but will ignore"
        loop

main = do
  getResp url
```

This just downloads the data, I haven't yet looked into actually
decompressing. My plan is to convert this fixpoint call into a conduit
and pipe the data trhough uncompression -- the conduit xml parser that
is quite neat -- whatever processing I want. Fingers crossed.
