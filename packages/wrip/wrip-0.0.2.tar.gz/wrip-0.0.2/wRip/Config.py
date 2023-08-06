#Please set any configuration needed below
#If the configurations are correct, but aren't being registered
#by the Rippers.py, please submit an issue on the github page. However, please
#remove any personal info from the config file, such as usernames or passwords.



#Instagram [CREDENTIALS]
instaUser = ''
instaPass = ''

#Instagram [IG-Scraper]
#Remember History
logStatus = 'True'

#Youtube-DL
#Template used to store files, directory, filename.
ytdloutputTemplate = '-o "wRipper/Rips/Youtube/%(uploader)s/%(title)s - %(id)s - %upload_date.%(ext)s"'
#Default Handlers Used
ytdlhandlerTemplate = '--no-check-certificate -f 137/248/136+140'
#Create custom history/log files for different categories. Add .txt to category name. After each edit run, python3 Config.py
history = ['history.txt', 'car.txt', 'talk.txt','help.txt']
#WGET
wgetHandlers = ''

#Standard
#Rip WIKI Pages [BETA]
wikiStatus = 'False'

#Mac/Linux Only
#Open Config.py Inside of wRipper
configStatus = 'True'






## ** Don't adjust anything below this point!!! **
import os.path
for item in history:
    if os.path.isfile('wRipper/Cache/Youtube/'+item):
        pass
    else:
        open('wRipper/Cache/Youtube/'+item, 'w').close
