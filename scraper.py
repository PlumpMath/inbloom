# coding: utf-8
"""
Parse RSS and scrape articles from the Femail category.
Strip newline and multiple whitespace then split by word
Pickle this list to a file for the Bloom Filter
"""

from urllib2 import urlopen
import feedparser
from bs4 import BeautifulSoup
import re
import pickle

urlopen('http://www.dailymail.co.uk/femail/index.rss').read()

f=feedparser.parse('http://www.dailymail.co.uk/femail/index.rss')

print "Entries: %r" %len(f.entries)

femail_words = []

for entry in f.entries:
    l = entry.link
    page = urlopen(l).read()
    soup = BeautifulSoup(page)
    try:
        article_text= [k.text.strip() for k in soup.find(class_='article-text wide').find_all('p')]
        cleaned_string = ""
        for p in article_text:
            p = p.replace('\n','')
            cleaned_string += ' ' + re.sub(' +',' ', p)
        femail_words.extend(cleaned_string.split(' '))
    except:
        pass

print len(femail_words)
f=open('femail_words.list', 'w')
pickle.dump(femail_words, f)
f.close()