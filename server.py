#!/usr/bin/env python3
import traceback
import socket
import pickle

import common
import unpickler

@unpickler.UnpicklerFromFunction
def safepickle(module, name):
    '''This filter will avoid any builtins, such as `exec`'''
    return module != 'builtins'

class Server(object):
    def __init__(self, host: str = common.HOST, port: int = common.PORT,
        safe: bool = False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = addr = (host, port)
        self.socket.bind(addr)
        self.timeout = 1
        self.safe = safe

        if safe:
            self.loads = safepickle.loads
        else:
            self.loads = pickle.loads

    def mainloop(self):
        print('Server mainloop starting on %s' % (self.address,))
        print('Safe mode is:', 'ON' if self.safe else 'OFF')
        print('Press Ctrl + C to stop the server.')
        try:
            while True:
                self.socket.settimeout(self.timeout)

                try:
                    data, addr = self.socket.recvfrom(2048)
                except socket.timeout:
                    continue

                try:
                    object = self.loads(data)
                except:
                    traceback.print_exc()
                    print('\n[info] Error was catched, server still running.\n')
                    continue

                print('Got a message from:', addr, '/ type:', type(object))
                print(' ', object)

                if object == common.STOP:
                    break

        except KeyboardInterrupt:
            print('EXIT')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default=common.HOST)
    parser.add_argument('--port', type=int, default=common.PORT)
    parser.add_argument('--safe', action='store_true',
        description='try to avoid exploits on unpickling')
    args = parser.parse_args()

    server = Server(args.host, args.port, safe=args.safe)
    server.mainloop()
