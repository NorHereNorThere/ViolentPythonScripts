import nmap
import argparse

def nmapScan(tgtHost, tgtPort):
    nmScanObj = nmap.PortScanner()
    nmScanObj.scan(tgtHost,tgtPort)
    
    state=nmScanObj[tgtHost]['tcp'][int(tgtPort)]['state']
    print(f"[*] {tgtHost} tcp/ {tgtPort} {state}")


    #A more flexible way to perform a nmap scan is as:
    #   nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PS 21,23,80,3389')
    #So the above would be:
    #   nmScanObj.scan(hosts=tgtHost, arguments=f'-PS {tgtPort}')
    # New comment this for sync
    
def main():
    parser = argparse.ArgumentParser(description='Scan Target host and ports')

    parser.add_argument('-t','--target',type=str,help='Specify Target Host')
    parser.add_argument('-p','--ports',type=str,help='Specify Target Port. Multiple ports have to be seperated by commas')

    options = parser.parse_args()

    tgtHost = options.target
    tgtPorts = str(options.ports).split(',')
    
    if (tgtHost == None) | (tgtPorts[0] == None):
        parser.print_help()
        return
    
    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
    main()