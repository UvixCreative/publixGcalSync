# publixGcalSync
Sync Publix work schedule from Oasis with my Google Calendar account

# Disclaimer
THIS IS NOT MAINTAINED AND IS NOT RECOMMENDED TO RUN ON YOUR OWN.

I only really posted this for the sake of archiving some of my old code. This is very insecure, and it probably doesn't even work anymore.

# More information

This is a very minor project I wrote in 2018 or so to make sure that my weekly work schedule appeared on my Google Calendar. This is very messy, and it was only really built for myself, so probably don't use this. I only skimmed through it before uploading it here changing a few things.

This just uses a web scraper (selenium) to literally spin up a Firefox window in an X desktop (on Linux), punch in the raw, plaintext credentials gathered from a file on the local filesystem, then grab the information from the HTML grid and format it into a readable timestamp for the Google Calendar API.

Again, this is very insecure, and it likely doesn't work anymore because I haven't worked at Publix in a few years. Oasis has probably changed or been replaced, which would definitely break this script.

It did work for me while I was there though, so that was fun.
