# Run this file tu setup your telegram account storage
# Complete the authorization process
# More info https://docs.pyrogram.org/intro/setup.html

from pyrogram import Client
from pyrogram.types import Message
from app.core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH

if __name__ == '__main__':
    app = Client(':memory:', TELEGRAM_API_ID, TELEGRAM_API_HASH)

    SESSION_STRING = ''

    with app:
        print('Save this in SESSION_STRING environment variable')
        print('SESSION_STRING\n')
        SESSION_STRING = app.export_session_string()
        print(SESSION_STRING)
        print('\n')

    client = Client(SESSION_STRING, TELEGRAM_API_ID, TELEGRAM_API_HASH)

    @client.on_message()
    def cid_handler(_: Client, message: Message):
        print(f'CHANNEL ID {message.chat.id}')

    print('Send some text in your channel and save channel id in CID environment variable')
    print('PRESS Ctrl^c to stop')
    client.run()
