import feedparser
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar 
import time
import os

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders= [('User-agent','Mozilla')]

bbcRSSFeed = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')

numberstories=[len(bbcRSSFeed)]
FeedLinks=[]
FeedTitles=[]

for post in bbcRSSFeed.entries:
    #print post.title 
    #print post.link + "\n"
    FeedLinks.append(post.link)
    FeedTitles.append(post.title)
    
limit=2
counter=0
paraStringList = []

for i in FeedLinks:
    print i
    continue
    #if counter<FeedLinks: #displays the content of every link
    if counter<limit:
        print "["+i +"]"
        newpage = urlopen(i)
        soup = BeautifulSoup(newpage)
        text = soup.select('.story-body p') #content of the news story
        print (text)
        counter+=1
    
            
    
        


