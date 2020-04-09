import argparse
import socket
import threading
#from socket import setdefaulttimeout, socket
#from threading import Semaphore, Thread

screenLock = threading.Semaphore(value=1)

def connScan(tgtHost,tgtPort):
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        #connSkt.send()
        results = connSkt.recv(1024)
        
        screenLock.acquire()

        print(f'[+] {tgtPort} TCP Open')
        print(f'[+] {results}')
    
    except Exception as e:
        screenLock.acquire()
        print(f'[-] {tgtPort} TCP Closed, Exception Reported: {e}')

    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost,tgtPorts):
    
    '''
    # If using in VLANs for testing, resolving addresses are unnecessary
    
    try:
        tgtIP = gethostbyname(tgtHost)
    
    except:
        print('[-] Cannot resolve ',tgtHost,': Unknow host')
        return
    
    try:
        tgtName = gethostbyaddr(tgtHost)
        print('\n[+] Scan Results for: ', tgtName[0])
    
    except:
        print('\nScan Results for: ', tgtHost)
   '''
    socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = threading.Thread(target=connScan(tgtHost,int(tgtPort)))
        t.start()
        #print('Scanning port ',tgtPort)
        #connScan(tgtHost,int(tgtPort))
   
def main():
    parser = argparse.ArgumentParser(description='The program scans provided IP and Ports')

    parser.add_argument('-t','--target',type=str,help='Specify Target Host')
    parser.add_argument('-p','--ports',type=str,help='Specify Target Port. Multiple ports have to be seperated by commas')

    options = parser.parse_args()

    tgtHost = options.target
    tgtPorts = str(options.ports).split(',')

    if (tgtHost == None) | (tgtPorts[0] == None):
        parser.print_help()
        return
    else:
        portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
