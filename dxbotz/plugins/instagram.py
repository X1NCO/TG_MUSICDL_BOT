# Copyright (C) 2023 DX-MODS
#Licensed under the  AGPL-3.0 License;
#you may not use this file except in compliance with the License.
#Author ZIYAN
#if you use our codes try to donate here https://www.buymeacoffee.com/ziyankp

from pyrogram import filters, Client as Dxbotz
import bs4, requests
from config import LOG_GROUP, DUMP_GROUP
@Dxbotz.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming, group=1)
async def link_handler(Dxbotz, message):
    link = message.matches[0].group(0)
    try:
        m = await message.reply_text("⏳")
        url= link.replace("instagram.com","ddinstagram.com")
        url=url.replace("==","%3D%3D")
        if url.endswith("="):
           dump_file=await message.reply_video(url[:-1])
        else:
            dump_file=await message.reply_video(url)
        if 'dump_file' in locals():
           await dump_file.forward(DUMP_GROUP)
        await m.delete()
    except Exception as e:
        try:
            if "/reel/" in url:
               getdata = requests.get(url).text
               soup = bs4.BeautifulSoup(getdata, 'html.parser')
               meta_tag = soup.find('meta', attrs={'property': 'og:video'})
               content_value = meta_tag['content']
               dump_file=await message.reply_video(f"https://ddinstagram.com{content_value}")
            elif "/p/" in url:
                 getdata = requests.get(url).text
                 soup = bs4.BeautifulSoup(getdata, 'html.parser')
                 meta_tag = soup.find('meta', attrs={'property': 'og:image'})
                 content_value = meta_tag['content']
                 dump_file=await message.reply_photo(f"https://ddinstagram.com{content_value}")
        except Exception as e:
            await message.reply_text(f"https://ddinstagram.com{content_value}")
            if LOG_GROUP:
               await Dxbotz.send_message(LOG_GROUP,f"Instagram {e} {content_value}")
            ##optinal 
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @dxziyan")

        finally:
            if 'dump_file' in locals():
               if DUMP_GROUP:
                  await dump_file.forward(DUMP_GROUP)
            await m.delete()
