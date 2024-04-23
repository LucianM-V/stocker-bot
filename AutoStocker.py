import asyncio

import discord
import requests
from bs4 import BeautifulSoup
from discord import Intents
from discord.ext import tasks

# Replace with your bot token
YOUR_BOT_TOKEN = "MTE0MzM0OTE2ODMxNjg3NDgwMg.GsTvZb.O9bvASPnrZFr-zDWLkKUIChrx3sgf0ZWAnQiu4"

# Replace with the website URL
TARGET_URL = "https://store.ctr-electronics.com/pigeon-2/"

# Replace with the out of stock text
STOCK_STATUS_TEXT = "out of stock"

# Replace with the in stock text
IN_STOCK_TEXT = "Quantity"

# Replace with the channel ID
CHANNEL_ID = 1144509373113176144

intents = Intents.default()
intents.message_content = True  # Enable message content intent

client = discord.Client(intents=intents)
previous_stock_status = None  # To keep track of previous stock status

@tasks.loop(seconds=60)  # Check every 60 seconds
async def check_stock_status():
    global previous_stock_status

    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    current_stock_status = None

    # Check if the "Out of stock" text is found anywhere in the HTML
    if STOCK_STATUS_TEXT in soup.text:
        current_stock_status = "OUT_OF_STOCK"
    elif IN_STOCK_TEXT in soup.text:
        current_stock_status = "IN_STOCK"

    # Check if the stock status changed and send a message
    if previous_stock_status != current_stock_status:
        previous_stock_status = current_stock_status

        channel = client.get_channel(CHANNEL_ID)

        # Send message based on current stock status
        message = ""
        if current_stock_status == "OUT_OF_STOCK":
            message = " **Stock Alert:** Item is out of stock!"
        elif current_stock_status == "IN_STOCK":
            message = " **Stock Update:** Item is back in stock!"

        await channel.send(message)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await asyncio.sleep(5)  # Add a delay to ensure channel is available
    check_stock_status.start()


client.run(YOUR_BOT_TOKEN)
