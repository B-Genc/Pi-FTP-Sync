#Importing Adafruit_CharLCD library and Configuring LCD
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCD(27,22,25,24,23,18,16,2,4)

#Importing other things like FTP and datetime tags
import ftplib
from datetime import datetime
import sys, time, json, os, os.path

#Loading config.json file
if (os.path.isfile('config.json') == True):
    cfgfile = open('config.json','r')
    config = json.load(cfgfile)
    cfgfile.close()
else: #If there is no config, ask for info
    server = raw_input("Server ip: ")
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    directory = raw_input("Directory: ")
    debug = raw_input("Debug Output(y/n)?:")
    config = {'server':server,
              'username':username,
              'password':password,
              'directory':directory,
              'debug':debug}
    cfgfile = open('config.json','w')
    json.dump(config,cfgfile)
    cfgfile.close()

#Functions:
def genFileCache():
    cache = list(os.listdir(config['directory']))
    return cache

def debug(text):
    if (config['debug'] == 'y'):
        print(text)

def disp(text, delay=None):
    lcd.clear()
    lcd.message(text)
    if (delay != None):
        time.sleep(delay)

def status(message):
    lcd.clear()
    lcd.message("  " + datetime.now().strftime('%b %d %H:%M') + "\n" + message)


#Declaring FTP
ftp = ftplib.FTP(config['server'])

try:
    ftp.login(config['username'],config['password'])
    debug("Login Successful to " + config['server'])
    disp("Connected to:\n" + config['server'],1)
except ftplib.all_errors:
    debug("Cannot connect to " + config['server'])
    disp("Connection Error\n" + config['server'],1)
    status("Connection Error")
    sys.exit()

localfiles = list(genFileCache()) #Declares localfiles as filelist   
remotefiles = ftp.nlist() #Getting filelist from server  
#Checking what server has more than local, and queuing to download
downloadList = list(set(remotefiles) - set(localfiles))

if (len(downloadList) == 0):
    debug("All files up to date, exiting...")
    disp("All files are\nup to date!",2)
    status("   All Synced")
    sys.exit()

itemCount = len(downloadList) #Total number of items to be downloaded
connFailCount = 0 #Will be used in except block to not continiously try
                  #connecting to server

lcd.blink(True)   #To show activity
for i in range(itemCount):
    try:
        fileName = downloadList[i]
        currentCount = i + 1 #i will start with 0, so this is for humans.
        debug(str(currentCount) + "/" + str(itemCount) + " Downloading " + fileName)
        disp(str(currentCount)+"/"+str(itemCount)+'\nDownloading ')
        ftp.retrbinary('RETR ' + fileName, open(config['directory'] + fileName,'wb').write)
    except:
        disp("    DOWNLOAD\n     FAILED",2)
        if connFailCount >= 3:
            break
        else:
            connFailCount += 1

lcd.blink(False)
disp("   Syncing...")
localfiles = list(genFileCache())
downloadList = list(set(remotefiles) - set(localfiles))
if (connFailCount >= 3):
    disp("   Connection\n     Failed")
    status("  Conn. Failed")
elif (len(downloadList) > 0):
    disp(str(len(downloadList)) + " FILES\n NOT DOWNLOADED",3)
    status(" Some Issues...")
elif (len(downloadList) == 0):
    status("   All Synced")
else:
    status(" Unknown Issue?")