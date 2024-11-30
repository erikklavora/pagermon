# A program made by Shane (Shaggs) Rees to use PDW's email function into python.
# pip install aiosmtpd
# pip install clint
# pip install requests

""" To get Started
Options -> SMTP / email settings
Setting set to all messages
SMTP Host 127.0.0.1
Port 8826
To can be set as anything 
From can be set as anything

Mail options select
Address, Time, Date, Bitrate, Message

Notification set to messages 
"""
import asyncio
from datetime import datetime
import email
from clint.textui import puts, colored
import time
from aiosmtpd.controller import Controller
import requests

class CustomHandler:
    def __init__(self):
        self.frag = ""

    async def handle_DATA(self, server, session, envelope):
        mime_message = email.message_from_bytes(envelope.content)
        message = mime_message.get_payload()
        
        try:
            flexcode, a, b, bitrate, msg = message.split(' ', 4)
            when = int(time.time())
            flexcode = "00"+flexcode
            msg = msg.strip()
            bitrate = str(bitrate)
            
            if bitrate == "1600":
                self.frag = msg
                puts(colored.yellow(flexcode), newline=False)
                puts(" [", newline=False)
                puts(colored.green(when), newline=False)
                puts("] ", newline=False)
                puts(msg)
                apost(flexcode, msg, when)
            elif bitrate == "1601":
                msg = self.frag + msg
                puts(colored.yellow(flexcode), newline=False)
                puts(" [", newline=False)
                puts(colored.green(when), newline=False)
                puts("] ", newline=False)
                puts(msg)
                apost(flexcode, msg, when)
                
            return '250 Message accepted for delivery'
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return '500 Error processing message'

def apost(flexcode, msg, when):
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'apikey': "5P43S420PVO07Q6D3VE0TTS0", #pagermon APIKey
        'User-Agent': 'PagerMon pdw2pagermon.py',
    }
    params = {
        "address": flexcode,
        "message": msg,
        "datetime": when,
        "source": "POZIVNIK 4",
    }
    requests.post('http://pager.pocsag112.org/api/messages', data=params, headers=headers)

async def main():
    handler = CustomHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=8826)
    
    # Start the SMTP server
    try:
        controller.start()
        print(f"SMTP server started on {controller.hostname}:{controller.port}")
        
        # Keep the server running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        controller.stop()
    except Exception as e:
        print(f"Server error: {e}")
        controller.stop()

if __name__ == '__main__':
    asyncio.run(main())
