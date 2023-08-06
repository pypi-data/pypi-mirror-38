import os
#Create All Rip Dirs
os.mkdir('Rips')
os.mkdir('Rips/Wiki')
os.mkdir('Rips/Youtube')
os.mkdir('Rips/Reddit')
os.mkdir('Rips/Instagram')
os.mkdir('Rips/Instagram/Stories')
os.mkdir('Rips/Instagram/Profiles')
#Create All Cache Dirs
os.mkdir('Cache')
os.mkdir('Cache/Instagram')
os.mkdir('Cache/Instagram/instagram-scraper')
os.mkdir('Cache/Youtube')
os.mkdir('Cache/Reddit')
#Create Cache CSVs
open('Cache/Reddit/download.csv', 'w').close
open('Cache/Reddit/history.csv', 'w').close
open('Cache/Reddit/recentscrape.csv', 'w').close
open('Cache/Youtube/log.txt', 'w').close
open('Cache/Instagram/instagram-scraper/history.txt', 'w').close

