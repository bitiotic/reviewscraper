#!/usr/bin/python
#
# Watch for changes to amazon/google product reviews.
#

CONFIG=".review-scraper"

VERBOSE=False

AMAZON_REVIEWS_URL="http://www.amazon.com/Bitiotic-Freeform-Backgammon/product-reviews/B00A7KD23K/ref=dp_db_cm_cr_acr_txt"
GOOGLE_PROD_URL="https://play.google.com/store/apps/details?id=com.bitiotic.freeform.android"

import sys
import urllib2
import BeautifulSoup
import md5
import os
import pickle

#_configFileName = os.path.join(os.path.expanduser("~"), CONFIG)
# XXX command line option for this (use explicit dir for running under cron)
_configFileName = os.path.join("/home/pat/", CONFIG)

# Picklable object that represents a review site (and what to scrape out of it)
class Site:
   def __init__(self, name, url, tag, attrs):
      self.name = name
      self.url = url
      self.tag = tag
      self.attrs = attrs

   def __hash__(self):
      # .tag and .attrs are not part of the identity
      return hash((self.name, self.url))

   def __eq__(self, other):
      # .tag and .attrs are not part of the identity
      return (self.name, self.url) == (other.name, other.url)

# Collect all the state to save in one place.  For each site, track checksum of reviews.
class Saved:
   PICKLEFMT=0

   def __init__(self):
      self.version = "review-scraper.py v0.0.5"
      self.sites = {}

   def addSite(self, site):
      self.updateSite(site, "unknown md5sum")

   def updateSite(self, site, csum):
      self.sites[site] = csum

   def save(self):
      """Save this object to the given file.  Existing contents will be obliterated."""
      with open(_configFileName, "w") as fileHandle:
         pickle.dump(self, fileHandle, Saved.PICKLEFMT)

   @staticmethod
   def load():
      """Load existing saved object from file, or create new object if no file exists."""
      if os.path.exists(_configFileName):
         with open(_configFileName, "r") as fileHandle:
            try:
               obj = pickle.load(fileHandle)
            except:
               obj = "Invalid Save File"
            if not isinstance(obj, Saved):
               raise RuntimeError, "Saved state corrupt, is not an instance of Saved"
            return obj
      else:
         return Saved()

# Retrive rough review text plus md5sum of reviewsa
def watchFor(label, url, tag, attrs):
   blurbs = scrapeChunks(label, url, tag, attrs)

   if VERBOSE:
      if not blurbs:
         print "No HTML found for ", tag, "+", attrs
      else:
         print blurbs

   # Compute md5 checksum of review so we can see if anything changed
   cx = md5.new()
   cx.update(blurbs)
   return (blurbs, cx.hexdigest())

def scrapeChunks(label, url, tag, attrs):
   req = urllib2.Request(url)
   response = urllib2.urlopen(req)
   content = BeautifulSoup.BeautifulSoup(response.read())

   #fh = open("/tmp/splat.html", "w")
   #fh.write(str(content.prettify()))
   #fh.close()

   chunks = content.body.findAll(tag, attrs=attrs)
   if not chunks:
      return None
   else:
      return "\n\n".join([c.text for c in chunks])

def addSite(saveState, name, url, tag, attrs):
   saveState.addSite(Site(name, url, tag, attrs))

def updateSites(saveState):
   for site, oldcx in saveState.sites.items():
      if VERBOSE:
         print "Checking", site.name, "..."
      newcx = watchFor(site.name, site.url, site.tag, site.attrs)
      saveState.updateSite(site, newcx)
      if VERBOSE:
         if newcx != oldcx:
            print "  Changed!"
         else:
            print "  No change"
      else:
         if newcx != oldcx:
            print "Reviews have changed (?) at", site.name

def main():
   state = Saved.load()
   try:
      if False:  # Set to 'True' to add these sites to the list.  Only needs to be done once.
         addSite(state, "Google", GOOGLE_PROD_URL, 'div', attrs={ 'class': 'review-body'})
         addSite(state, "Amazon", AMAZON_REVIEWS_URL, 'table', attrs={ 'id': 'productReviews' })

      updateSites(state)
   finally:
      state.save()
      
if __name__ == "__main__":
   sys.exit(main())

#eof
