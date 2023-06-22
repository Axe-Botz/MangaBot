import random
from pyrogram import Client, filters
from pyrogram.types import Message

from Asura import asura as app

# Handler function for the /start command
@app.on_message(filters.command("start"))
def start(_, message: Message):
    message.reply_text("Welcome to AnimePFPBot! Send /get_pfp to get a random anime character profile picture.")

# Handler function for the /get_pfp command
@app.on_message(filters.command("get_pfp"))
def get_pfp(_, message: Message):
    # Fetch a random anime pfp from a list of URLs
    anime_pfps = [
        "https://api.myanimelist.net/v2",
        # Add more URLs here
    ]
    
    # Select a random pfp URL
    pfp_url = random.choice(anime_pfps)
    
    # Send the pfp to the user
    message.reply_photo(photo=pfp_url)
