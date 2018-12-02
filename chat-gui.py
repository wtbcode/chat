from tkinter import *
#import easygui as e
import asyncio
import json
new_messages = 0
window = Tk()
window.geometry("500x500") 
window.title("Chat GUI")
window.iconbitmap(r'icon.ico')
title = Label(window,text = "Chat:")
title.config(font=("Courier", 44))
title.place(x=250,y=10)
title.pack()
chat_stream = Text(window, height= 20, width= window.winfo_width())
chat_stream.pack()
message_label = Label(window,text = "Message:")
message_label.config(font=("Courier", 12))
message_label.place(x=250,y=80) 
message_label.pack()
message_box = Text(window, height= 2, width = window.winfo_width())
message_box.pack()

def post():
    message = message_box.get("1.0",END)
    request = {"action" : "send", "user" : user, "message" : message}
    transport.write(json.dumps(request).encode())
    message_box.delete(1.0,END)
def post_enter(event):
    post()
    return "break"
message_box.bind('<Return>',post_enter)
button = Button(window,text="Comment",command=post)
button.pack()

class ChatClientProtocol(asyncio.Protocol):

    def connection_lost(self, exc):
        print('The server closed the connection')

    def data_received(self, data):
        request = json.loads(data.decode())
        chat_stream.insert(END,'{}: {}'.format(request["user"], request["message"]))
        global new_messages
        new_messages += 1
        window.title("Chat GUI [{}]".format(str(new_messages)))

async def run_tk(window, interval=0.05):
    try:
        while True:
            window.update()
            await asyncio.sleep(interval) 
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise

async def main(host, port):
    loop = asyncio.get_running_loop()
    global transport
    transport, protocol = await loop.create_connection(lambda: ChatClientProtocol(), host, port)
    task = loop.create_task(run_tk(window))
    await task
    
user = "tux"
host = "127.0.0.1"
port = 64000    
asyncio.run(main(host, port))
