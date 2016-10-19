title: Transfer files to your phone over wifi
date: 2016-09-29 03:54
tags: unix
category:
slug: transfer-files-to-your-phone-over-wifi
author: Chris Perivolaropoulos

So here is a neat trick to very quickly transfer files to your phone
over wifi (http). On your computer download `qrencode`. It should be
in all major package managers. Also make sure you have python
installed. On your phone install a QR code reader.

Open a terminal and navigate to the folder where your file is. Then
run this on *OSX*:

    ifconfig en0 | awk 'BEGIN{FS=" "} /^\t*inet /{print "http://"$2":8000"}' | xargs qrencode -o /tmp/url_local_qr.png && open /tmp/url_local_qr.png && python -m SimpleHTTPServer

or this on *linux* (didn't try it so comment if there was a problem):

    ifconfig wlan0 | awk 'BEGIN{FS=" "} /^\t*inet /{print "http://"$2":8000"}' | xargs qrencode -o /tmp/url_local_qr.png && dispaly /tmp/url_local_qr.png && python -m SimpleHTTPServer

You should be presented with a QR code. Scan it with your phone and
you should have access to your computer's files!
