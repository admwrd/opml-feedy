# opml-feedy
Read OPML Podcast feeds. Archives feed episodes in its own folder.

# Overview

OPML Feedy reads your OPML file and does the following

For each feed in your OPML file

* Create a new folder for that feed
* Create a feed.sh script to fetch feed episodes

OPML Feedy uses "youtube-dl" as the file fetcher, but this can be changed at the top of the file by setting the `FEED_DL_APP` to something else.

You can also change which shell interpreter is used (default is *bash*).

And finally, you can change what the actual shell script is named in each folder.

# Installing

No need for pip. You only need to have `youtube-dl` (or an alternative if you want) installed on your system.

Download the Python file and run!

# Running

1. `cd` to the directory you want to save your feeds.
2. `cp` or `mv` the `opml_feedy.py` file to that directory.
3. Pass the OPML file as an argument.
4. Run!


```bash
python opml_feedy.py MySavedPodcastFeeds.opml
```

# After Running

Provided you are using the default installation, and have youtube-dl already installed...

You now have a bunch of folders for each of your feeds! Now you just need to run the scripts to download each feed!

From the folder that contains all of your feed folders (and OPML Feedy), you can do something like

```bash
for d in `ls -d -- */`; do
    cd "$d";
    echo "Getting feed for $d";
    ls -l feed.sh;
    cd ..;
done
```

This goes into each directory and runs the `feed.sh` script to download the feed files.

**Note that this just loops through one feed at a time. So it may take a while to fully backup your feeds. Feel free to change it up how you want!**


# Warning!

Again, OPML Feedy creates a new folder for each feed. This is done in the folder you have OPML Feedy saved. So make sure you have it in a good location!

This project is provided as-is, with no warranty or claims of benefit. Do with it what you want. I'm not responsible if something goes wrong with your files / computer / life.

