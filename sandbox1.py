from ftplib import FTP
import time, sys
ftp = FTP("ServerIP") # Declaring server IP
ftp.login('supercow','amazingpassword')  # Logging in with credentials
files = []
dates = []
files = ftp.nlst()
files = (filter(lambda k: '.zip' in k, files)
#out = [w.replace('.zip','') for w in files]

#Formatting is as follows : YYYYMMDDHHMMSS

#for i in range(0, len(files)-1):
#    dates[i] = time.strptime(files[i], "%Y%m%d%H%M%S")

#print(files)
#print(dates)

ftp.quit()