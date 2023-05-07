import os
from config import GENIUS_API
from pyrogram import filter
from pyrogram.types import Messages
from dxbotz import Dxbotz
from lyricsgenius import genius
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong


api = genius.Genius(GENIUS_API,verbose=False)


@Dxbotz.on_message(filters.command(['lyrics','genius'],prefixes=['/','!']) 
    & (filters.group | filters.private) 
    & ~ filters.edited)
async def lyrics(dxbotz:Dxbotz,msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(
            text='__Please specify the query...__', 
        )

    r_text = await msg.reply('__Searching...__')
    song_name = msg.text.split(None, 1)[1]

    lyric = api.search_song(song_name)

    if lyric is None:return await r_text.edit('__No lyrics found for your query...__')

    lyric_title = lyric.title
    lyric_artist = lyric.artist
    lyrics_text = lyric.lyrics

    try:
        await r_text.edit_text(f'__--**{lyric_title}**--__\n__{lyric_artist}\n__\n\n__{lyrics_text}__\n__Extracted by @DxSotifyDLbot')

    except MessageTooLong:
        with open(f'downloads/{lyric_title}.txt','w') as f:
            f.write(f'{lyric_title}\n{lyric_artist}\n\n\n{lyrics_text}')

        await r_text.edit_text('__Lyric too long. Sending as a text file...__')
        await msg.reply_chat_action(
            action='upload_document'
        )
        await msg.reply_document(
            document=f'downloads/{lyric_title}.txt',
            thumb='dxbotz/utils/dxspotifyld.jpg',
            caption=f'\n__--{lyric_title}--__\n__{lyric_artist}__\n\n__Extracted by @DxSotifyDLbot'
        )

        await r_text.delete()
        
        
        os.remove(f'downloads/{lyric_title}.txt')
