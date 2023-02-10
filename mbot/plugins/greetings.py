from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup, Message
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP,SUDO_USERS, Mbot, AUTH_CHATS, DATABASE_URL, name, START_PIC
from mbot.utils.database import Database
import os
from os import execvp,sys , execl,environ
from sys import executable
from apscheduler.schedulers.background import BackgroundScheduler
db = Database(DATABASE_URL, name)
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

@Mbot.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"👋 Hai {user.mention} \n𝙸'𝚖 𝙰 𝚂𝚒𝚖𝚙𝚕𝚎 𝙵𝚒𝚕𝚎 𝚁𝚎𝚗𝚊𝚖𝚎+𝙵𝚒𝚕𝚎 𝚃𝚘 𝚅𝚒𝚍𝚎𝚘 𝙲𝚘𝚟𝚎𝚛𝚝𝚎𝚛 𝙱𝙾𝚃 𝚆𝚒𝚝𝚑 𝙿𝚎𝚛𝚖𝚊𝚗𝚎𝚗𝚝 𝚃𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 & 𝙲𝚞𝚜𝚝𝚘𝚖 𝙲𝚊𝚙𝚝𝚒𝚘𝚗 𝚂𝚞𝚙𝚙𝚘𝚛𝚝!"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("👼 𝙳𝙴𝚅𝚂 👼", url='https//github.com/DX-MODS/')
        ],[
        InlineKeyboardButton('📢 𝚄𝙿𝙳𝙰𝚃𝙴𝚂', url='https://t.me/dxmodsupdates'),
        InlineKeyboardButton('🍂 𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url='https://t.me/DXMODS_Support')
        ],[
        InlineKeyboardButton('🍃 𝙰𝙱𝙾𝚄𝚃', url='https//github.com/DX-MODS/'),
        InlineKeyboardButton('ℹ️ 𝙷𝙴𝙻𝙿', url='https//github.com/DX-MODS/')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)

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

HELP = {
    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
    "Spotify": "Send **Spotify** Track/Playlist/Album/Show/Episode's Link. I'll Download It For You.",
    "Deezer": "Send Deezer Playlist/Album/Track Link. I'll Download It For You.",
    "Jiosaavn": "Send Any Query eg /saavn faded",
    "SoundCloud": "Trying to impliment",
    "Group": "Coming Soon"
}


@Mbot.on_message(filters.command("help"))
async def help(_,message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]

    await message.reply_text(f"Hello **{message.from_user.first_name}**, I'm **@DxSpotifyDlbot**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))

@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_,query):
    i = query.data.replace("help_","")
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Back",callback_data="helphome")]])
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text = text,reply_markup=button)

@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    await query.message.edit(f"Hello **{query.from_user.first_name}**, I'm **@DxSpotifyDlbot**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))
