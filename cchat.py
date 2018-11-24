#!/usr/bin/env python3 -u

'''
Chat client.

USAGE

  cchat.py USER
  cchat.py USER [HOST/IP]
  cchat.py USER [HOST/IP] [PORT]

  USER    - The name you want to be identified as.

  HOST/IP - The host or IP address the chat server is listening on.
            Default: 127.0.0.1

  PORT    - The TCP port the chat server is listening on.
            Default: 64000
'''

import json
import signal
import sys
import asyncio

class ChatClientProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        print('The server closed the connection')

    def data_received(self, data):
        request = json.loads(data.decode())
        print(("\r" + request["user"] + ": " + request["message"]).ljust(80, " "))
        print("> ", end = "")

async def main(host, port):
    linebuffer = []
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(lambda: ChatClientProtocol(), host, port)
    print("> ", end = "")
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        line = line.rstrip()
        linebuffer.extend(list(line))
        if len(linebuffer) > 0 and linebuffer[-1] == ";":
            request = {"action" : "send", "user" : user, "message" : "".join(linebuffer[:-1])}
            transport.write(json.dumps(request).encode())
            linebuffer.clear()
        else:
            print("> " + "".join(linebuffer), end = "")

if len(sys.argv) < 2:
    print("Usage: cchat.py USER [HOST/IP] [PORT]")
    sys.exit(1)

user = sys.argv[1] 
host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
port = int(sys.argv[3]) if len(sys.argv) > 3 else 64000
signal.signal(signal.SIGINT, signal.SIG_DFL)
asyncio.run(main(host, port))
