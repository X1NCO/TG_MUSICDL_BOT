from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot, AUTH_CHATS, DATABASE_URL, name
from mbot.utils.database import Database
import os
from os import execvp,sys , execl,environ
from sys import executable
from apscheduler.schedulers.background import BackgroundScheduler
db = Database(DATABASE_URL, name)
def restar():
    print("restarting")
    os.system("rm -rf /tmp/*")
    if not os.path.exists("/tmp/thumbnails/"):
       os.mkdir("/tmp/thumbnails/")
    execl(executable, executable, "-m", "mbot")
scheduler = BackgroundScheduler()
scheduler.add_job(restar, "interval", minutes=15)
scheduler.start()

@Mbot.on_message(filters.command("start"))
async def start(client,message):
    reply_markup = [[
        InlineKeyboardButton(
            text="Bot Channel", url="https://t.me/DxSpotifyDlbot"),
        InlineKeyboardButton(
            text="Repo",
            url="https://github.com/DX-MODS/SpotifyDL/"),
        InlineKeyboardButton(text="Help",callback_data="helphome")
        ],
        [
            InlineKeyboardButton(text="Donate",
            url="https://www.buymeacoffee.com/ziyankp"),
        ]]
    if LOG_GROUP:

        invite_link = await client.create_chat_invite_link(chat_id=(int(LOG_GROUP) if str(LOG_GROUP).startswith("-100") else LOG_GROUP))
        reply_markup.append([InlineKeyboardButton("LOG Channel", url=invite_link.invite_link)])
    if message.chat.type != "private" and message.chat.id not in AUTH_CHATS and message.from_user.id not in SUDO_USERS:
        return await message.reply_text("This Bot Will Not Work In Groups Unless It's Authorized.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))
    return await message.reply_text(f"Hello {message.from_user.first_name}, I'm a Adanced Music Downloader Bot. I Currently Support Download from Youtube,spotify,deezer,saavan.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","mbot"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")
   
@Mbot.on_message(filters.command("users") & filters.private )
async def sts(c: Client, m: Message):
    user_id=m.from_user.id
    if user_id in OWNER_ID:
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
