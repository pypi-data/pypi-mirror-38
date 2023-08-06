import os
import sys
import re
import requests
import datetime
import csv
import Config
import json
                                ##GET CONFIG JSON DATA##
with open('/Users/zacharysimpson/wRipper/config.json') as f:
    config_json = json.load(f)
    for item in config_json['Youtube-dl']:
      ytdloutputTemplate = item['ytdloutputTemplate']
      ytdlhandlerTemplate = item['ytdlhandlerTemplate']
      ytdlhistory = item['ytdlhistory']

    for item in config_json['Instagram-Scraper']:
      igslogStatus = item['igslogStatus']

    for item in config_json['Instagram']:
      instaUser = item['instaUser']
      instaPass = item['instaPass']

    for item in config_json['WGET']:
        wgetHandlers = item['wgetHandlers']

    for item in config_json['Standard']:
        wikiStatus = item['wikiStatus']

    for item in config_json['Unix']:
        configStatus = item['configStatus']



                                ##MENU##
def menu():
    print('1: Reddit')
    print('2: Imgur')
    print('3: GFYCAT')
    print('4: Instagram')
    print('5: Youtube-dl')
    print('6: WGET')
    if Config.wikiStatus == 'True':
        print('7: Wiki[BETA]')
    if Config.configStatus == 'True':
        print('8: Config')
    userAction = input('Enter a Number: ')


    if userAction == '1':
        ripReddit()
    elif userAction == '2':
        ripImgur()
    elif userAction == '3':
        ripGfycat()
    elif userAction == '4':
        ripInstagram()
    elif userAction == '5':
        ripYoutubeDL()
    elif userAction == '6':
        wget()
    if Config.wikiStatus == 'True':
        if userAction == '7':
            ripWiki()
    if Config.configStatus == 'True':
        if userAction == '8':
            config()
menu()
                                    ##CONFIG MENU##
def config():
    os.system('nano wRipper/Config.py')
    menu()

                                      ##IMGUR##
def ripImgur():
    from imgurpython import ImgurClient
    regex = re.compile(r'\.(\w+)$')
    def get_extension(link):
        ext = regex.search(link).group()
        return ext

    try:
        album_id = input('ID: ')
    except IndexError:
        raise Exception('Please specify an album id')

    client_id = 'f778feba14cc5b0'
    client_secret = '98480e3edbb0a177f88ec45353a23bcd73c0a159'
    client = ImgurClient(client_id, client_secret)

    img_lst = client.get_album_images(album_id)
    for i in img_lst:
        file_ext = get_extension(i.link)
        resp = requests.get(i.link, stream=True)

        # create unique name by combining file id with its extension
        file_name = i.id + file_ext
        with open(file_name, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                f.write(chunk)
    menu()

                                        ##REDDIT##

def ripReddit():
    import psaw
    import pandas as pd
    from os import listdir
    timeNowO = datetime.datetime.now()
    timeNow = str(timeNowO)[:10]
    api = psaw.PushshiftAPI()

    #Get Sub-Reddit Info (Name-Term-Filter-Limit)
    subIN = input('SubReddit: ')
    qIN = input('Term: ')
    limIN = input('File Limit: ')
    submissions = api.search_submissions(
                                    subreddit = subIN,
                                    q = qIN,
                                    limit = limIn,
                                    filter = ['url'],)

    #Create Main CSV
    csvRed = 'wRipper/Cache/Reddit/recentscrape.csv'
    df1 = pd.DataFrame([c.d_ for c in submissions])
    df1.to_csv(csvRed, mode='w')
    #Open CSV To Read
    df2 = pd.read_csv(csvRed)
    #Delete Default Columns
    df2.drop('created', axis = 1, inplace = True)
    df2.drop('created_utc', axis = 1, inplace = True)
    df2.drop('Unnamed: 0', axis = 1, inplace = True)

    #Create New/Edited CSV
    df2.to_csv(csvRed, mode='w', index = False)
    #Where to download posts too
    downDir = 'wRipper/Rips/Reddit/'+subIN+'-'+qIN+'-'+timeNow
    recentScrape = 'wRipper/Cache/Reddit/recentscrape.csv'
    redditDownloads = 'wRipper/Cache/Reddit/download.csv'
    redditHistory = 'wRipper/Cache/Reddit/history.csv'

    with open(redditHistory, 'r') as t1, open(recentScrape, 'r') as t2:
     fileone = t1.readlines()
     filetwo = t2.readlines()

    with open(redditDownloads, 'w') as downloadsW, open(redditHistory, 'a') as historyW:
         for line in filetwo:
             if line not in fileone:
                 downloadsW.write(line)
                 historyW.write(line)
             elif line in fileone:
                 print(line+' Has already been ripped: Skipping')


    os.mkdir(downDir)
    os.system('wget -no-check-certificate -i '+redditDownloads+' -P '+downDir)
    dirList = os.listdir(downDir)

    for file in dirList:
        fileName,fileExt = os.path.splitext(file)

        if fileExt == '.mp4' or fileExt == '.jpg' or  fileExt == '.gif' or fileExt == '.png':
            pass
        else:
            os.remove(os.path.join(downDir, file))

    menu()


                                         ##Wikipedia##
def ripWiki():
    from bs4 import BeautifulSoup
    url = input('Wiki Link: ')
    tableNum = int(input('Table Number: '))
    filename = url.replace('https://en.wikipedia.org/wiki/', '').replace('_', ' ')
    response = requests.get(url, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table', class_="wikitable")[tableNum]
    rows = table.select('tbody > tr')
    header = [th.text.rstrip() for th in rows[0].find_all('th')]
    with open('wRipper/Rips/Wiki/'+filename+'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows[1:]:
            data = [th.text.rstrip() for th in row.find_all('td')]
            writer.writerow(data)
    menu()
                                                        ##Youtube##
def ripYoutubeDL():
    ytLink = input('URL: ')
    ytdlHandler = input('YT-DL Handler(s): ')
    print('1 = Obey Log: ')
    print('2 = No Log: ')
    ytdlLog = input('Enter A Number: ')

    if ytdlLog == '1':
       os.system('youtube-dl '+Config.ytdloutputTemplate+' --download-archive wRipper/Cache/Youtube/history.txt '+Config.ytdlhandlerTemplate+' '+ytdlHandler+' '+ytLink)
    elif ytdlLog == '2':
       os.system('youtube-dl '+Config.ytdloutputTemplate+' '+Config.ytdlhandlerTemplate+' '+ytdlHandler+' '+ytLink)
    menu()
                                               ##InstaGram##
def ripInstagram():
    print('1: Profile [Looter]')
    print('2: Followers Stories')
    print('3: Profile [IG-Scraper]')

    instaChoice = float(input('Enter A Number: '))

    if instaChoice == 1:
      instaProfile = input('Profile: ')
      os.chdir('wRipper/Rips/Instagram/Profiles')
      os.system('instaloader --fast-update --no-video-thumbnails --no-profile-pic --no-captions --no-metadata-json --filename-pattern={profile}/{date_utc}_UTC --l='+Config.instaUser+' -p='+Config.instaPass+' '+instaProfile)
    elif instaChoice == 2:
      os.chdir('wRipper/Rips/Instagram/Stories')
      os.system('instaloader --no-video-thumbnails --no-metadata-json --dirname-pattern={profile} --filename-pattern={date_utc}_UTC --l='+Config.instaUser+' -p='+Config.instaPass+' :stories')
    elif instaChoice == 3:
        print('1: Profile')
        print('2: Batch File')
        profileOrBatch = input('Enter a Number: ')

        if profileOrBatch == '1':
            instaProfile = input('Profile: ')
            profileDir = 'wRipper/Rips/Instagram/Profiles/'+instaProfile
            #Checks if Config File is set to obey history
            if Config.logStatus == 'True':
                IgscraperHandlers = '--latest-stamps wRipper/Cache/Instagram/instagram-scraper/history.txt'
                os.system('instagram-scraper '+instaProfile+' -u '+Config.instaUser+' -p '+Config.instaPass+' -t video image -d wRipper/Rips/Instagram/Profiles -n '+IgscraperHandlers)
            #Checks if Config File is set to NOT obey history
            elif Config.logStatus == 'False':
                os.system('instagram-scraper '+instaProfile+' -u '+Config.instaUser+' -p '+Config.instaPass+' -t video image -d wRipper/Rips/Instagram/Profiles -n')

        elif profileOrBatch == '2':
            batchDir = input('Batch File Location: ')
            #Checks if Config File is set to obey history
            if Config.logStatus == 'True':
                IgscraperHandlers = '--latest-stamps wRipper/Cache/Instagram/instagram-scraper/history.txt'
                os.system('instagram-scraper -f '+batchDir+' -u '+Config.instaUser+' -p '+Config.instaPass+' -t video image -d wRipper/Rips/Instagram/Profiles -n '+IgscraperHandlers)
            #Checks if Config File is set to NOT obey history
            elif Config.logStatus == 'False':
                os.system('instagram-scraper -f '+batchDir+' -u '+Config.instaUser+' -p '+Config.instaPass+' -t video image -d wRipper/Rips/Instagram/Profiles -n')
    menu()
                            #Fix Default Dir
##      os.chdir("/Users/zacharysimpson/wRipper/Rips/Instagram/Stories")
##      for root, dirs, files in os.walk(".", topdown = False):
##          for file in files:
##              if file.endswith('.xz'):
##                  print(os.path.join(root, file))
##                  os.remove(os.path.join(root, file))


def wget():
    url = input('URL: ')
    wgetHandlers = input('WGET Handlers: ')
    os.system('wget -no-check-certificate '+wgetHandlers+' '+Config.wgetHandlers+' '+url+' -P wRipper/Rips/WGET')
