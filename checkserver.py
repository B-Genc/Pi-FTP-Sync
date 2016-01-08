#This is an utility for checking connection to FTP server.
import sys
from ftplib import FTP

if (len(sys.argv) != 4): # It is 4 instead of 3 because argv includes checkserver.py as well
    print("Invalid args\nUsage: python checkserver.py <server ip> <username> <password>")
    sys.exit()

ServerIP = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

ftp = FTP(ServerIP)

try:
    ftp.login(username,password)
    print("Login Successful")
except:
    print("Login Failed")