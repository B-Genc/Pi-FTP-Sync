from ftplib import FTP
import sys, time, operator, json
DIR = '/Location/Here/'
f = open(DIR + 'last.json','r')
localfiles = json.load(f)
print(localfiles)
f.close()

ftp = FTP('ServerIP')

try:
    ftp.login('supercow','amazingpassword')
    print("Success")
except ftplib.all_errors:
    print("Error")
    sys.exit()

files = [] #Creating empty list for files
files = ftp.nlst() #Adding file names from FTP
files = filter(lambda k: '.zip' in k, files) #Exclude no .zip
diff = []
diff = (list(set(files)- set(localfiles))) #Find differences
if len(diff)==0:
    print("All files are up to date")
print("Downloading " + files[1])
#ftp.retrbinary('RETR ' + files[1], open(files[1],'wb').write)
print("Downloaded")
f = open(DIR + 'last.json','w')
json.dump(files,f)
f.close()

ftp.quit()
print("bye")