from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from dxbotz import Dxbotz
import requests 

import os


API = "https://apis.xditya.me/lyrics?song="

@Dxbotz.on_message(filters.text & filters.command(["lyrics"]) & filters.private)
async def sng(bot, message):          
          mee = await message.reply_text("`Searching`")
          try:
              song = message.text.split(None, 1)[1].lower().strip().replace(" ", "%20")
          except IndexError:
              await message.reply("give me a query eg `lyrics faded`")
          chat_id = message.from_user.id
          rpl = lyrics(song)
          await mee.delete()
          try:
            await mee.delete()
            await message.reply(rpl)
          except Exception as e:                            
             await message.reply_text(f"lyrics does not found for `{song}` ", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url = f"https://t.me/dxmodsupdates")]]))
          finally:
            await message.reply("Check out @DxSpotifyDl(music)  @dxziyan(owner)")



def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = fin["lyrics"]
        return text
