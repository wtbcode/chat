#!/usr/bin/env python3

'''
Chat server.

USAGE

  schat.py 
  schat.py [HOST/IP]
  schat.py [HOST/IP] [PORT]

  HOST/IP - The host or IP address to listen on.
            Default: (all available)

  PORT    - The TCP port to listen on or 0 to choose an available port.
            Default: 64000
'''

import signal
import sys
import asyncio

class ChatServerProtocol(asyncio.Protocol):
    def __init__(self, connections):
        self.connections = connections

    def connection_made(self, transport):
        self.connections += [transport]
        self.transport = transport

    def connection_lost(self, exc):
        self.connections.remove(self.transport)

    def data_received(self, data):
        message = data.decode()
        for connection in self.connections:
            connection.write(data)

async def main(host, port, connections):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: ChatServerProtocol(connections), host, port)
    for socket in server.sockets:
        addr = socket.getsockname()
        print("Listening on {}:{}".format(addr[0], addr[1]))

    await server.serve_forever()

signal.signal(signal.SIGINT, signal.SIG_DFL)
host = sys.argv[1] if len(sys.argv) > 1 else ""
port = int(sys.argv[2]) if len(sys.argv) > 2 else 64000
connections = []
asyncio.run(main(host, port, connections))
