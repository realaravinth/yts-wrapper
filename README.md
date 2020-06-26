*Note: Development is discontinued because I lost interest and also this doesn't come with any warrenties so use it at your own discretion.*

# yts-wrapper
Django-based, transmission-cli powered wrapper website for https://yts.mx that's capable of downloading movies on to the server. Basically, popcorntime.sh but on the server!


## Table of contents:

- [Status](#status)
- [Dependencies:](#dependencies)

## Status
In the current state, the Django backend can contact yts.mx's API and retreive information on movies. It can also use that data to get the top-rated subtitle off of yifysubtitles(webscraping, couldn't find API).
Upon clicking `download`, it would then initiate the download with transmission-cli. It should then proceed to process that with ffmepg and convert to a streamable format(MP4) and convert the subtitles to VTT. 
It does these things but it's not complete.

## Dependencies:
  * Transmission-cli
  * Django(3.0)
  * Requires a Linux machine(Linux shell scripts handle downloading and processsing)
