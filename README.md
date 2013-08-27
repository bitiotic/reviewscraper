App Review Scraper
------------------

Bare bones script for noticing changes (i.e., new reviews) in the reviews
associated with an Android app at Google or Amazon.

This is meant to be run from a cron job once a day or so, to inform
you of new reviews.  Currently it shouts about any change, and is not
tested on apps with lots of reviews.

Usage
-----

Edit the AMAZON_REVIEWS_URL and/or GOOGLE_PROD_URL at the top of
main.py.

Edit the _configFilePath directory.

Edit the main method to add the sites to the save file (change 'False'
to 'True').  Run main.py once to initialize the save file.

Setup a cron entry to run main.py (or use the review-scraper.sh wrapper).


TODO
----

* Remove hardcoded config path (default to current directory?)
* Add command-line options (--config, --addsite, --verbose)
* Test on apps with more than 2 reviews (pages of reviews?  Sort by date?)
* Better summary of what has changed.
* Move hard-coded Bititoc URLs to documentation
* Add some doc
