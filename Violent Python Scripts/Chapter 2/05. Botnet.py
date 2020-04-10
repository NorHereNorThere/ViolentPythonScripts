import argparse
from pexpect import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
    
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except pxssh.ExceptionPxssh as e:
            print(e)
            print(f'[-] Error Connecting')

    def sendCommand(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.sendCommand(command)
        print(f'[*] Output from {client.host}')
        print(f'[+] {output}') 

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)


botNet = []
addClient('127.0.0.1', 'root', 'toor')
addClient('127.0.0.1', 'root', 'toor')
addClient('127.0.0.1', 'root', 'toor')

botnetCommand('uname -v')
botnetCommand('cat /etc/issue')
    
