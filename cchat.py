#!/usr/bin/env python3

'''
Chat client.

USAGE

  cchat.py 
  cchat.py [HOST/IP]
  cchat.py [HOST/IP] [PORT]

  HOST/IP - The host or IP address the chat server is listening on.
            Default: 127.0.0.1

  PORT    - The TCP port the chat server is listening on.
            Default: 64000
'''

import signal
import sys
import asyncio

class ChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        print('The server closed the connection')

async def main(host, port):
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(lambda: ChatClientProtocol(), host, port)

    while True:
        message = input("> ")
        transport.write(message.encode())

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 64000
signal.signal(signal.SIGINT, signal.SIG_DFL)
asyncio.run(main(host, port))
