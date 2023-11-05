# Copyright (C) 2023 DX_MODS
#Licensed under the  AGPL-3.0 License;
#you may not use this file except in compliance with the License.
#Author ZIYAN

from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
import random
from dxbotz.utils.txt import dx
from dxbotz.utils.database import db
from config import START_PIC


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"👋 Hai {user.mention} \n𝙸'𝚖 𝙰 𝚊𝚍𝚟𝚊𝚗𝚌𝚎𝚍 𝚖𝚞𝚜𝚒𝚌 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝𝚜 𝚂𝚙𝚘𝚝𝚒𝚏𝚢 𝚍𝚎𝚎𝚣𝚎𝚛 𝚢𝚘𝚞𝚝𝚞𝚋𝚎 𝚜𝚊𝚊𝚟𝚗!"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("📺 𝙳𝙴𝚅𝚂 📺", callback_data='dev')
        ],[
        InlineKeyboardButton('📣 𝚄𝙿𝙳𝙰𝚃𝙴𝚂', url='https://t.me/Makima_update'),
        InlineKeyboardButton('🎧 𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url='https://t.me/makimamusic_support')
        ],[
        InlineKeyboardButton('👓 𝙰𝙱𝙾𝚄𝚃', callback_data='about'),
        InlineKeyboardButton('ℹ️ 𝙷𝙴𝙻𝙿', callback_data='help')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)  

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f""" Hey {query.from_user.mention}🫶🏻 \n𝙸'𝚖 𝙰 𝚊𝚍𝚟𝚊𝚗𝚌𝚎𝚍 𝚖𝚞𝚜𝚒𝚌 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 for 𝚂𝚙𝚘𝚝𝚒𝚏𝚢 D𝚎𝚎𝚣𝚎𝚛 Y𝚘𝚞𝚝𝚞𝚋𝚎 S𝚊𝚊𝚟A𝚗! """,
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("📺 𝙳𝙴𝚅𝚂 📺", callback_data='dev')                
                ],[
                InlineKeyboardButton('📣 𝚄𝙿𝙳𝙰𝚃𝙴𝚂', url='https://t.me/Makima_update'),
                InlineKeyboardButton('🎧 𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url='https://t.me/makimamusic_support')
                ],[
                InlineKeyboardButton('👓 𝙰𝙱𝙾𝚄𝚃', callback_data='about'),
                InlineKeyboardButton('ℹ️ 𝙷𝙴𝙻𝙿', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=dx.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=dx.ABOUT_TXT,            
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=dx.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
