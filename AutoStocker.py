import asyncio

import discord
import requests
from bs4 import BeautifulSoup
from discord import Intents
from discord.ext import tasks


YOUR_BOT_TOKEN = "MTE0MzM0OTE2ODMxNjg3NDgwMg.GsTvZb.O9bvASPnrZFr-zDWLkKUIChrx3sgf0ZWAnQiu4"

# Define a list of products
products = [
    # Add dictionaries for 9 more products following the same format
    {
        #Pidgeon 2
        "url": "https://store.ctr-electronics.com/pigeon-2/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "pidgeons"
    },
    {
        #Spark Max
        "url": "https://www.revrobotics.com/rev-11-2158/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "Spark Max"
    },
    {
        #Mini Power Module
        "url": "https://www.revrobotics.com/rev-11-1956/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "MPMs"
    },
    {
        #Kraken x60
        "url": "https://store.ctr-electronics.com/kraken-x60/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "Krakens"
    },
    {
        #Kraken Hex Adapter
        "url": "https://wcproducts.com/pages/stock-status",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "8mm SplineXS to 1/2",
        "stock_status_text_in_stock": "(WCP-1118) In Stock",
        "name": "Kraken Hex Adapter"
    },
    {
        #NEO
        "url": "https://www.revrobotics.com/rev-21-1650/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "NEOs"
    },
    {
        #PDH
        "url": "https://www.revrobotics.com/rev-11-1850/",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "Enter your email address",
        "stock_status_text_in_stock": "Quantity",
        "name": "PDH"
    },
    {
        #Limelight 3g
        "url": "https://www.andymark.com/products/limelight-3g?via=Z2lkOi8vYW5keW1hcmsvV29ya2FyZWE6Ok5hdmlnYXRpb246OlNlYXJjaFJlc3VsdHMvJTdCJTIycSUyMiUzQSUyMmxpbWVsaWdodCUyMiU3RA",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "This item is currently out of stock",
        "stock_status_text_in_stock": "Quantity",
        "name": "Limelight 3G"
    },
    {
        #RIO 2.0
        "url": "https://www.andymark.com/products/ni-roborio-2",
        "channel_id": 1144509373113176144,
        "stock_status_text_out_of_stock": "This item is currently out of stock",
        "stock_status_text_in_stock": "Quantity",
        "name": "RIO 2.0"
    },


]

intents = Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
previous_stock_status = {}  # Dictionary to store previous status for each product


@tasks.loop(seconds=120)  # Check every 60 seconds
async def check_stock_status():
  global previous_stock_status

  for product in products:
    response = requests.get(product["url"])
    soup = BeautifulSoup(response.content, "html.parser")

    current_stock_status = None

    # Check for stock status based on product information
    if product["stock_status_text_out_of_stock"] in soup.text:
      current_stock_status = "OUT_OF_STOCK"
    elif product["stock_status_text_in_stock"] in soup.text:
      current_stock_status = "IN_STOCK"
    else:
        current_stock_status = "OUT_OF_STOCK"

    # Check if the stock status changed and send a message
    if previous_stock_status.get(product["url"]) != current_stock_status:
      previous_stock_status[product["url"]] = current_stock_status

      channel = client.get_channel(product["channel_id"])

      # Send message based on current stock status
      message = ""
      if current_stock_status == "OUT_OF_STOCK":
        message = f" **Stock Alert:** {product['name']} is out of stock!"
      elif current_stock_status == "IN_STOCK":
        message = f" **Stock Alert:** {product['name']} is in stock!"

      await channel.send(message)


@client.event
async def on_ready():
  print(f"Logged in as {client.user}")
  await asyncio.sleep(5)  # Add a delay to ensure channel is available
  check_stock_status.start()


client.run(YOUR_BOT_TOKEN)
