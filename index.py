import logging

import boto3

from functions import server_open_channel
from util import socket_manager

import discord

from constants.bot_constant import bot_user


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s')

@bot_user.bot.event
async def on_ready():
    socket_manager.socket_event_dispatch("server_close_dispatch", 3570).start()
    await server_open_channel.from_config()
    logging.info(f"We have logged in as {bot_user.bot.user}")
    request = boto3.client("ec2").describe_spot_instance_requests()
    print(request)

bot_user.bot.load_extension("commands.command_handler")
bot_user.bot.run("YOUR_TOKEN")
