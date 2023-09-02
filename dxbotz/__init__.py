# Copyright (C) 2023 DX_MODS
#Licensed under the  AGPL-3.0 License;
#you may not use this file except in compliance with the License.
#Author ZIYAN
from pyrogram import Client
import os 
from os import environ,sys,mkdir,path
import logging
from sys import executable
#from Python_ARQ import ARQ
from aiohttp import ClientSession
import shutil
from config import API_ID, API_HASH, BOT_TOKEN, AUTH_CHATS

# Log
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(message)s",
    handlers = [logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
    
class Dxbotz(Client):
    def  __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir="./cache/",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=30
        )
    async def start(self):
        # os.system(f"rm -rf ./cache/")
        # os.system(f"mkdir ./cache/")
        global BOT_INFO
        await super().start()
        BOT_INFO = await self.get_me()
        if not path.exists('/tmp/thumbnails/'):
            mkdir('/tmp/thumbnails/')
        for chat in AUTH_CHATS:
            await self.send_photo(chat,"https://telegra.ph/Bot-Started-09-02","**𝑀𝑎𝑘𝑖𝑚𝑎 𝑆𝑡𝑎𝑟𝑡𝑒𝑑 🎧**")
        LOGGER.info(f"Bot Started As {BOT_INFO.username}\n")
    
    async def stop(self,*args):
        await super().stop()
        LOGGER.info("Bot Stopped, Bye.")
