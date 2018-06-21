#!/usr/bin/env python3
import traceback
import socket
import pickle

import common

class Server(object):
    def __init__(self, host: str = common.HOST, port: int = common.PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = addr = (host, port)
        self.socket.bind(addr)
        self.timeout = 1

    def mainloop(self):
        print('Server mainloop starting on %s' % (self.address,))
        print('Press Ctrl + C to stop it')
        try:
            while True:
                self.socket.settimeout(self.timeout)

                try:
                    data, addr = self.socket.recvfrom(2048)
                except socket.timeout:
                    continue

                try:
                    object = pickle.loads(data)
                except:
                    traceback.print_exc()
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
    args = parser.parse_args()

    server = Server(args.host, args.port)
    server.mainloop()
