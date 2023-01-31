from pyrogram import Client, filters
import requests 
import wget
@Client.on_message(filters.command('saavn') & filters.text)
async def song(client, message):
    try:
       args = message.text.split(None, 1)[1]
    except:
        return await message.reply("/saavn requires an argument.")
    if args.startswith(" "):
        await message.reply("/saavn requires an argument.")
        return ""
    pak = await message.reply('Downloading...')
    try:
        r = requests.get(f"https://saavn.me/search/songs?query={args}")
    except Exception as e:
        await pak.edit(str(e))
        return
    sname = r.json()[1]["name"]
    slink = r.json()[4]["downloadUrl"]
    ssingers = r.json()[0]["primaryArtists"]
    album_id = r.json()[0]["id"]
    img = r.json()[2]["image"]
    thumbnail = wget.download(img)
    file = wget.download(slink)
    ffile = file.replace("mp4", "m4a")
    os.rename(file, ffile)
    await pak.edit('Uploading...')
    await message.reply_audio(audio=ffile, title=sname, performer=ssingers,caption=f"{sname} - from saavn",thumb=thumbnail)
    os.remove(ffile)
    os.remove(thumbnail)
    await pak.delete()
