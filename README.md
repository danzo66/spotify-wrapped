Every year, my friend always makes a mashup of everyones Spotify Wrapped playlists by comparing any songs that more than two people have in their Top 100!

Last December, I decided to one-up him by automating it!


This program is really badly commented, and I can only apologise for that! I wrote it in a day or so, and didn't expect that I would end up sharing it!

I think there may also be a few places where I have gone about things in a rather round-about way, and I have since realised I could have just used a built-in function.

However, I choose to look at that as gaining a deeper understanding of the functions and learning more about Python, rather than me making things more complicated than they need to be!


The first program to run is loaddata.py. This takes in Excel spreadsheets and converts them to numpy arrays.
The data must be in the B column, and start from B2. B2 must be the name of the playlist.
The data can just be copied and pasted from Spotify into a spreadsheet - it sorts out the URL!
This does take a long time to run, as it has to search the source code of the webpage for the title, since Spotify is funny about automations.

The second program to run is spotifywrapped.py. This takes in the .npy arrays and sorts them into two master playlists.
squadwrapped is based on the songs in common, artistwrapped is based on the artists in common.
artistfreq is the data on all the artists in common.