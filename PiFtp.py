#LCD Configuration
import Adafruit_CharLCD as LCD
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#Importing Libraries
from ftplib import FTP
from datetime import datetime
import sys, time, json

#Config
DownloadsDir = '/enter/download/directory/here'
ConfigFile = '/enter/cache/directory/here/last.json'
ftpserver = 'example.com'
username = 'supercow'
password = 'amazingpassword'
debug = True # Type false if you don't want anything to be printed

#Small functions to clean the code
def debug(txt): #Just a print statement, bool == true
    if debug == True:
        print(txt)

def disp(txt, delay=None): #Simple display manager
    lcd.clear() #Clears LCD
    lcd.message(txt) #Prints LCD message
    if (delay != None):
        time.sleep(delay) #If there is delay declared, delay

def status(message): #Generally to be used when program is not active
    lcd.clear()
    lcd.message(datetime.now().strftime('%b %d %H:%M') + "\n" + message)
    
ftp = FTP(ftpserver) #Declaring ftp server ip

try:
    ftp.login(username,password)
    debug("Login Successful")
    disp("Connected:\n"+ftpserver,1)
except ftplib.all_errors:
    debug("Login Failed, exiting...")
    disp("Failed:\n"+ftpserver,2)
    status("Err:Login Failed")
    sys.exit()

f = open(ConfigFile,'r')  # Opening Config file
localfiles = json.load(f) # Importing config file to list
debug("Imported.")
f.close() # Closing file

files = [] # Creating an empty list for filelist from server
files = ftp.nlst() #Receiving the file list from server
files = filter(lambda k: '.zip' in k, files) #Excluding anything other than zip

difference = [] #List for difference between local files and remote files
difference = list(set(files) - set(localfiles))

if (len(difference) == 0): #See if there is no file to sync
    disp("All files are\nup to date!",3)
    status("   All Synced")
    debug("All files up to date, exiting...")
    sys.exit()

#Starting to download missing files
downloaded = []
filesLeft = len(difference)
connFailCount = 0
for i in range(len(difference)):
    try:
        debug(str(i) + "/" + str(filesLeft) + " Left..\n" + difference[i])
        disp("Download Started\n"+difference[i],0.1)
        ftp.retrbinary('RETR ' + difference[i], open(DownloadsDir + difference[i],'wb').write)
        disp("File Downloaded\n"+difference[i],1)
        debug("File downloaded: " + difference[i])
        downloaded.append(difference[i])
    except:
        disp("Download failed\n"+difference[i],1)
        debug("Download failed : " + difference[i])
        if connFailCount >= 3:
            break
        else:
            connFailCount += 1

failed = []
failed = list(set(difference) - set(downloaded))

f = open(ConfigFile, 'w')
json.dump(downloaded,f)
f.close()
if (len(failed) == 0):
    disp("All files are\nup to date!",3)
    debug("All files are synchronized")
    status("   All Synced")
elif (connFailCount >= 3):
    status("Connection Error")
else:
    disp(str(len(failed)) + " failed to\ndownload.",3)
    debug(str(len(failed)) + " files are failed to download")
    status(str(len(failed))+" Down. Failed")
    
    