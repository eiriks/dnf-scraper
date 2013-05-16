#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2, sys, re
#from BeautifulSoup import BeautifulSoup
# or if your're using BeautifulSoup4:
from bs4 import BeautifulSoup

# next time use: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#parsing-only-part-of-a-document to only parse a prt of the document...


#
# script to scrape the emails from the Norwegian Authors´ Union - http://www.forfatterforeningen.no/english
#

url_base = 'http://www.forfatterforeningen.no'
start_url = 'http://www.forfatterforeningen.no/medlemmer-b'
urls_to_scrape = []

emails = []

def scrape(url):
    print url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    
    # two columns matches this query
    columns = soup.find_all("div", { "class" : "field-content" })
    
    #loop thrugh them
    for col in columns:
        for tag in col.find_all(text=re.compile("\(.+\)")): # "\(.+\)" mateches (a)
            #print tag, len(tag.split())
            
            # how long the strings containing (.) is matters
            if len(tag.split()) == 3:
                try:                        # the short email line contains empty space, proably in this format: 'name (a) host.no'
                    tag.split(" ")  
                    #print tag.split(" ")[-3] + '@' + tag.split(" ")[-1]
                    emails.append(tag.split(" ")[-3] + '@' + tag.split(" ")[-1])
                except:                     # the short email line dosnt contains empty space, proably in this format: 'name(a)host.no'
                    #print tag.split()[-1].split('(a)')[0] + '@' + tag.split()[-1].split('(a)')[1]
                    emails.append(tag.split()[-1].split('(a)')[0] + '@' + tag.split()[-1].split('(a)')[1])
            elif len(tag.split()) == 5:
                #print tag.split()[-3] + tag.split()[-2] + tag.split()[-1]
                #print tag.split()[-3] + '@' + tag.split()[-1]
                emails.append(tag.split()[-3] + '@' + tag.split()[-1])
            elif len(tag.split()) == 4:
                #print tag.split()[-3] + '@' + tag.split()[-1]
                emails.append(tag.split()[-3] + '@' + tag.split()[-1])
            else:
                print "pokker, her er det ugler i mosen.."
                print tag, len(tag.split())



# let's get strted:
soup = BeautifulSoup(urllib2.urlopen(start_url).read())

# collect all urls and append to urls_to_scrape
abc_liks_div = soup.find(id="block-menu-menu-meny-medlemmer").find_all('a', href=True) # cool! find and find_all can be chained!
for link in abc_liks_div:
    urls_to_scrape.append(url_base+link['href'])

# run the scraper
for url in urls_to_scrape:
    scrape(url)


#print emails, len(emails), len(set(emails))
with open('DnF_epostliste.txt', 'wb') as f:
    for email in set(emails):
        f.write(email + '\n')


# with open('file_to_write', 'w') as f:
#             f.write('file contents')

sys.exit("ferdig")
