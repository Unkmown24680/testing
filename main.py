from telethon import TelegramClient, events
import os
from colorama import Fore

class Forwarder:
    def start(self):
        os.system("cls")
        
        api_id = int(os.environ.get('API_ID'))  # Retrieving API ID from Heroku Config Vars
        api_hash = os.environ.get('API_HASH')  # Retrieving API hash from Heroku Config Vars
        phone = os.environ.get('PHONE_NUMBER')  # Retrieving phone number from Heroku Config Vars

        if not all([api_id, api_hash, phone]):
            print(f"{Fore.RED}Missing API ID, API hash, or phone number. Please check your Config Vars.{Fore.RESET}")
            return

        client = TelegramClient(phone, api_id, api_hash)
        client.start()

        bot_chat_id = os.environ.get('BOT_CHAT_ID')  # Retrieve bot chat ID from Heroku Config Vars

        @client.on(events.NewMessage(chats='YOUR_CHANNEL_ID'))
        async def forward_to_bot(event):
            try:
                message = await event.get_message()
                await client.forward_messages(bot_chat_id, message)
                print("Message forwarded to bot successfully.")
            except Exception as e:
                print(f"Error forwarding message to bot: {e}")

        with client:
            client.run_until_disconnected()

if __name__ == "__main__":
    forwarder = Forwarder()
    forwarder.start()