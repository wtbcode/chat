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
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(ChatServerProtocol, host, port)
    for socket in server.sockets:
        addr = socket.getsockname()
        print("Listening on {}:{}".format(addr[0], addr[1]))

    await server.serve_forever()

host = sys.argv[1] if len(sys.argv) > 1 else ""
port = int(sys.argv[2]) if len(sys.argv) > 2 else 64000
signal.signal(signal.SIGINT, signal.SIG_DFL)
asyncio.run(main(host, port))
