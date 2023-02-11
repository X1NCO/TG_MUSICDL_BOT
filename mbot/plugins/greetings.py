from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup, Message
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP,SUDO_USERS, Mbot, AUTH_CHATS
import os
from os import execvp,sys , execl,environ
from sys import executable
from apscheduler.schedulers.background import BackgroundScheduler
OWNER_ID = 1612304850
def restar():
    print("restarting")
    os.system("rm -rf /tmp/*")
    if not os.path.exists("/tmp/thumbnails/"):
       os.mkdir("/tmp/thumbnails/")
    execl(executable, executable, "-m", "mbot")
scheduler = BackgroundScheduler()
scheduler.add_job(restar, "interval", minutes=15)
scheduler.start()

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","mbot"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")
   
@Mbot.on_message(filters.command("users") & filters.chat(OWNER_ID))
async def sts(c: Client, m: Message):
        total_users = await db.total_users_count()
        await m.reply_text(text=f"Total Users in DB: {total_users}", quote=True)

@Mbot.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")
