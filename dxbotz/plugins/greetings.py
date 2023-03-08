# Copyright (C) 2023 DX_MODS
#Licensed under the  AGPL-3.0 License;
#you may not use this file except in compliance with the License.
#Author ZIYAN
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup, Message
from pyrogram.raw.functions import Ping
from dxbotz import LOG_GROUP,SUDO_USERS, Dxbotz, AUTH_CHATS,OWNER_ID
import os
from os import execvp,sys , execl,environ
from sys import executable
#if you are facing auto bot off issues it is because you are server needs some traffic if bot is not used it will stop the container if you are deploying in uffizi pls remove # in the below codes
#from apscheduler.schedulers.background import BackgroundScheduler
#def restar():
#    print("restarting")
#    os.system("rm -rf /tmp/*")
#    if not os.path.exists("/tmp/thumbnails/"):
#       os.mkdir("/tmp/thumbnails/")
#    execl(executable, executable, "-m", "dxbotz")
#scheduler = BackgroundScheduler()
#scheduler.add_job(restar, "interval", minutes=10)
#scheduler.start()

@Dxbotz.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","dxbotz"])

@Dxbotz.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")
   
@Dxbotz.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")
