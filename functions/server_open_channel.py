import base64
import datetime
import json
import logging
import math

import discord.ui
from discord.ui import Item

from constants.bot_constant import bot_user
from util.boto3_manager import boto3_client


async def run(channel, template_id, version, min_ram, max_ram):
    await channel.send(embed=discord.Embed(title="Open Server", description="Click the button below to open the "
                                                                            "server, the server will close "
                                                                            "automatically"
                                                                            "when nobody has been online for up to 5 "
                                                                            "minuets", color=0x026fdb),
                       view=buttonView(channel, template_id=template_id, version=version, min_ram=min_ram, max_ram=max_ram))


class buttonView(discord.ui.View):

    def __init__(self, channel, *items: Item, template_id, version, min_ram, max_ram):
        super().__init__(*items)
        self.timeout = None
        self.channel = channel
        self.cooldown = 0
        self.template_id = template_id
        self.version = version
        self.min_ram = min_ram
        self.max_ram = max_ram

    @discord.ui.button(label="Open The Server", style=discord.ButtonStyle.primary, emoji="😎")
    async def button_callback(self, button, interaction):
        if not math.floor(datetime.datetime.now().timestamp() > self.cooldown):
            await interaction.response.send_message(
                f"This command is on cooldown for {self.cooldown - math.floor(datetime.datetime.now().timestamp())} seconds",
                ephemeral=True)
            return

        self.cooldown = math.floor(datetime.datetime.now().timestamp() + 300)
        boto3 = boto3_client()
        if boto3.is_open(channel=self.channel.id):
            await interaction.response.send_message("The server is already running!", ephemeral=True)
            return

        boto3.start_server(template_id=self.template_id, version=self.version, max_ram=self.max_ram,
                           min_ram=self.min_ram)
        await interaction.response.send_message("The Server is Opening. This Could Take A Couple Minuets.",
                                                ephemeral=True)
        logging.info(f"{interaction.user} Successfully Opened the Server")


async def from_config():
    with open("config.json", "r+") as file:
        data = json.load(file)

    for server in data["servers"]:
        await run(channel=bot_user.bot.get_channel(server["channelID"]),
        template_id=server["template_id"],
        version=server["version"],
        min_ram=server["min_ram"],
        max_ram=server["max_ram"])