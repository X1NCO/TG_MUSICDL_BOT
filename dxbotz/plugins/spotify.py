from pyrogram.errors import FloodWait,Forbidden,UserIsBlocked,MessageNotModified,ChatWriteForbidden, SlowmodeWait 
from asyncio import sleep
import time
from config import AUTH_CHATS, LOGGER, LOG_GROUP, BUG, ADMIN, MAINTENANCE
from dxbotz import Dxbotz
from pyrogram import filters,enums
from dxbotz.utils.mainhelper import parse_spotify_url,fetch_spotify_track,download_songs,thumb_down,copy,forward 
from dxbotz.utils.ytdl import getIds,ytdl_down,audio_opt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from os import mkdir
from os import environ
from shutil import rmtree
from random import randint
from mutagen import File
from mutagen.flac import FLAC ,Picture
from lyricsgenius import Genius 
from pyrogram.types import Message
from pyrogram.errors.rpc_error import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from pyrogram.errors import ChatAdminRequired
from requests import head
from requests.exceptions import MissingSchema
client = Spotify(auth_manager=SpotifyClientCredentials())
PICS = ("dxbotz/1162775.jpg mbot/danny-howe-bn-D2bCvpik-unsplash.jpg mbot/saurabh-gill-38RthwbB3nE-unsplash.jpg").split()
genius = Genius("api_key")
LOG_TEXT_P = """
ID - <code>{}</code>
Name - {}
"""
@Dxbotz.on_message(filters.incoming & filters.regex(r'https?://open.spotify.com[^\s]+') | filters.incoming & filters.regex(r'https?://spotify.link[^\s]+'), group=-2)
async def spotify_dl(Dxbotz,message: Message):
    if MAINTENANCE:
       await message.reply_text(f"Bot Is Under Maintenance ⚠️")
       return
    link = message.matches[0].group(0)
    if "https://spotify.link" in link:
        link = head(link).headers['location']
    if "https://www.deezer.com" in link:
       return
    if "https://youtu.be" in link:
          return await message.reply("301: Use @y2mate_api_bot Insted Of Me 🚫")
    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0],parsed_item[1]
    except Exception as e:
        pass
        cr =  await message.reply("417: Not Critical, Retrying Again  🚫")
        await  Dxbotz.send_message(BUG,f" Private r: Unsupported [URI](link) Not critical {message.chat.id}  {message.from_user.id} {message.from_user.mention}")   
        try:
            link = head(link).headers['location']
            parsed_item = await parse_spotify_url(link)
            item_type, item_id = parsed_item[0],parsed_item[1]
        except Exception as e:
            pass 
            await  Dxbotz.send_message(BUG,f" Private r: Unsupported [URI](link) Failed twice {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
            return await cr.edit(f"501: This URI Is Not Supported ⚠")
    if message.text.startswith("/thumb"):
       try:
          await Dxbotz.send_message(BUG,f"Thumb download requested from {message.from_user.mention}")
          if item_type == "track":
             item = client.track(track_id=item_id)
             alb = client.album(album_id=item['album']['id'],)
             await message.reply_document(alb['images'][0]['url'])
          elif item_type == "playlist":
               play = client.playlist(playlist_id=item_id,)
               await message.reply_document(play['images'][0]['url'])
          elif item_type == "album":
               alb = client.album(album_id=item_id,)
               await message.reply_document(alb['images'][0]['url'])
          elif item_type == "artist":
               art = client.artist(item_id)
               await message.reply_document(art['images'][0]['url'])
       except Exception as e:
           pass
           await message.reply("404: sorry, thumbnail download is not available for this track 😔")
           await Dxbotz.send_message(BUG,f" thumb 400 {e}")
       return 
    if message.text.startswith("/preview"):
          if item_type == "track":
             try:
                 await Dxbotz.send_message(BUG,f"Preview download requested from {message.from_user.mention}")
                 item = client.track(track_id=item_id)
                 await  message.reply_audio(f"{item.get('preview_url')}")
             except Exception as e:
                 pass
                 await message.reply("404: sorry, audio preview is not available for this track 😔")
                 await Dxbotz.send_message(BUG,e)
          return 
    try: 
       if item_type in ["https:","http:"]:
          cr =  await message.reply("417: Not Critical, Retrying Again  🚫")
          await sleep(1)
          return await cr.edit(f"501: This URI Is Not Supported ⚠")
    except Exception as e:
        pass
        await  Dxbotz.send_message(BUG,f" Private r: Unsupported http [URI](link) Failed twice {message.chat.id}  {message.from_user.id} {message.from_user.mention}")     
    u = message.from_user.id
    randomdir = f"/tmp/{str(randint(1,100000000))}"
    mkdir(randomdir)
    try:
        m = await message.reply_text(f"⏳")
        await message.reply_chat_action(enums.ChatAction.TYPING)
    except ChatWriteForbidden:
        pass
        chat=message.chat.id
        await Dxbotz.leave_chat(chat)
        k = await Dxbotz.send_message(-1001744816254,f"{chat} {message.chat.username} or {message.from_user.id}")
        await  k.pin()
        sp = f"I have left from {chat} reason: I Am Not  Admin "
        await Dxbotz.send_message(message.from_user.id,f"{sp}") 
    try:
        if item_type in ["show", "episode"]:
            items = await getIds(link)
            for item in items:
                cForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                sleeeps = await sleep (0.9)
                PForCopy = await message.reply_photo(item[5],caption=f"✔️ Episode Name : `{item[3]}`\n🕔 Duration : {item[4]//60}:{item[4]%60}")
                reply = await message.reply_text(f"sorry we removed support of  episode 😔 pls send other types album/playlist/track")
       
        elif item_type == "track":
            song = await fetch_spotify_track(client,item_id)
            try:
                item = client.track(track_id=item_id)
            except:
                pass
               
            try:
                if not item:
          
                    PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n\n[IMAGE]({song.get('cover')})\nTrack id:`{song['deezer_id']}`")
                else:
                     PForCopy = await message.reply_photo(item['album']['images'][0]['url'],caption=f"🎧 Title : `{song['name']}­­`\n🎤 Artist : `{song['artist']}`­\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n❗️Is Local:`{item['is_local']}`\n 🌐ISRC: `{item['external_ids']['isrc']}`\n\n[IMAGE]({item['album']['images'][0]['url']})\nTrack id:`{song['deezer_id']}`",
                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
            except:
                pass
                PForCopy = await message.reply_text(f"🎧 Title : `{song['name']}`\n­🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n\n[IMAGE]({song.get('cover')})\ntrack id:`{song['deezer_id']}`")
            try:
               path = await download_songs(item,randomdir)
            except Exception as e:
                pass
                await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
                await message.reply(e)
            thumbnail = await thumb_down(item['album']['images'][0]['url'],song.get('deezer_id'))
            try:
                audio = FLAC(path)
                audio["TITLE"] = f" {song.get('name')}"
                audio["ORIGINALYEAR"] = song.get('year')
                audio["YEAR_OF_RELEASE"] = song.get('year')
                audio["WEBSITE"] = "https://t.me/spotify_downloa_bot"
                audio["GEEK_SCORE"] = "9"
                audio["ARTIST"] = song.get('artist')                                                                            
                audio["ALBUM"] = song.get('album')
                audio["DATE"] = song.get('year')
                audio["DISCNUMBER"] =f" {item['disc_number']}"
                audio["TRACKNUMBER"] =f" {item['track_number']}"
                try:
                    audio["ISRC"] = item['external_ids']['isrc']
                except:
                    pass
                try:
                    songGenius = genius.search_song(song('name'), song('artist'))
                    audio["LYRICS"] = (songGenius.lyrics)
                except:
                    pass
                audio.save()
                audi = File(path)
                image = Picture() 
                image.type = 3
                if thumbnail.endswith('png'):
                   mime = 'image/png'
                else:
                     mime = 'image/jpeg'
                image.desc = 'front cover'
                with open(thumbnail, 'rb') as f: # better than open(albumart, 'rb').read() ?
                     image.data = f.read()

                audi.add_picture(image)
                audi.save()
            except:
                pass
            try:
                dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                AForCopy = await message.reply_audio(path,performer=f"{song.get('artist')}­",title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail, parse_mode=enums.ParseMode.MARKDOWN,quote=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
            except:
                pass
            if LOG_GROUP:
               await forward(PForCopy,AForCopy)
        elif item_type == "playlist":
            play = client.playlist(playlist_id=item_id,)
            tracks = client.playlist_items(playlist_id=item_id,additional_types=['track'], offset=0, market=None)   
            total_tracks = tracks.get('total')
            track_no = 1
            try:
                PForCopy = await message.reply_photo(play['images'][0]['url'],
                caption=f"▶️Playlist:{play['name']}\n📝Description:{play['description']}\n👤Owner:{play['owner']['display_name']}\n❤️Followers:{play['followers']['total']}\n🔢 Total Track:{play['tracks']['total']}\n\n[IMAGES]({play['images'][0]['url']})\n{play['uri']}")
            except Exception as e:
                pass
                PForCopy = await message.reply(f"▶️Playlist:{play['name']}\n📝Description:{play['description']}\n👤Owner:{play['owner']['display_name']}\n❤️Followers:{play['followers']['total']}\n🔢 Total Track:{play['tracks']['total']}\n\n[IMAGES]({play['images'][0]['url']})\n{play['tracks']['uri']}")
                await message.reply("are you sure it's a valid playlist 🤨?")
            
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('track').get('id'))
                item = client.track(track_id=track['track']['id'])
                try:
                   path = await download_songs(item,randomdir)
                except Exception as e:
                    pass
                    await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
                    await message.reply(e)
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                audio = FLAC(path)
                try:
                    audio["TITLE"] = f" {song.get('name')} "
                    audio["ORIGINALYEAR"] = song.get('year')
                    audio["YEAR_OF_RELEASE"] = song.get('year')
                    audio["WEBSITE"] = "https://t.me/spotify_downloa_bot"
                    audio["GEEK_SCORE"] = "9"
                    audio["ARTIST"] = song.get('artist')                                                                           
                    audio["ALBUM"] = song.get('album')
                    audio["DATE"] = song.get('year')
                    audio["discnumber"] =f" {item['disc_number']}"
                    audio["tracknumber"] =f" {item['track_number']}"
                    try:
                        audio["ISRC"] = item['external_ids']['isrc']
                    except:
                        pass
                    try:
                       songGenius = genius.search_song(song('name'), song('artist'))
                       audio["LYRICS"] = (songGenius.lyrics)
                    except:
                        pass
                except:
                     pass
                audio.save()
                audi = File(path)
                image = Picture()
                image.type = 3
                if thumbnail.endswith('png'):
                    mime = 'image/png'
                else:
                    mime = 'image/jpeg'
                image.desc = 'front cover'
                with open(thumbnail, 'rb') as f: # better than open(albumart, 'rb').read() ?
                   image.data = f.read()

                audi.add_picture(image)
                audi.save()
                try:
                    await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                    AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,parse_mode=enums.ParseMode.MARKDOWN,quote=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]])) 
                except:
                  pass
                track_no += 1
                if LOG_GROUP:
                   await forward(PForCopy,AForCopy)
           
        elif item_type == "album":
            alb = client.album(album_id=item_id,)
            try:
                PForCopy = await message.reply_photo(alb['images'][0]['url'],
                caption=f"💽Album: {alb['name']}\n👥Artists: {alb['artists'][0]['name']}\n🎧Total tracks{alb['total_tracks']}\n🗂Category: {alb['album_type']}\n📆Published on: {alb['release_date']}\n\n[IMAGE]({alb['images'][0]['url']})\n{alb['uri']}")
            except Exception as e:
                pass
                err = print(e)
                PForCopy = await message.reply(f"💽Album: {alb['name']}\n👥Artists: {alb['artists'][0]['name']}\n🎧Total tracks{alb['total_tracks']}\n🗂Category: {alb['album_type']}\n📆Published on: {alb['release_date']}\n\n[IMAGE]({alb['images'][0]['url']})\n{alb['uri']}")
            for track in alb['tracks']['items']:
                item = client.track(track_id=track['id'])
                song = await fetch_spotify_track(client,track.get('id'))
                try:
                   path = await download_songs(item,randomdir)
                except Exception as e:
                    pass
                    await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
                    await message.reply(e)
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                audio = FLAC(path)
                try:
                    audio["TITLE"] = f" {song.get('name')} "
                    audio["ORIGINALYEAR"] = song.get('year')
                    audio["YEAR_OF_RELEASE"] = song.get('year')
                    audio["WEBSITE"] = "https://t.me/spotify_downloa_bot"
                    audio["GEEK_SCORE"] = "9"
                    audio["ARTIST"] = song.get('artist')                                                                         
                    audio["ALBUM"] = song.get('album')
                    audio["DATE"] = song.get('year')
                    audio["discnumber"] =f" {item['disc_number']}"
                    audio["tracknumber"] =f" {item['track_number']}"
                    try:
                        audio["ISRC"] =f" {item['external_ids']['isrc']}"
                    except:
                        pass
                    try:
                        songGenius = genius.search_song(song('name'), song('artist'))
                        audio["LYRICS"] = (songGenius.lyrics)
                    except:
                       pass
                except:
                    pass
                audio.save()
                audi = File(path)
                image = Picture()
                image.type = 3
                if thumbnail.endswith('png'):
                   mime = 'image/png'
                else:
                    mime = 'image/jpeg'
                image.desc = 'front cover'
                with open(thumbnail, 'rb') as f: # better than open(albumart, 'rb').read() ?
                   image.data = f.read()

                audi.add_picture(image)
                audi.save()
                try:
                    AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,parse_mode=enums.ParseMode.MARKDOWN,quote=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
                except:
                    pass 
                if LOG_GROUP:
                   await forward(PForCopy,AForCopy)
           
        elif item_type == "artist":
             art = client.artist(item_id)
             try:
                 PForCopy = await message.reply_photo(art['images'][0]['url'],
                 caption=f"👤Artist: **{art['name']}­**\n❤️Followers:{art['followers']['total']}­\n🎶Generes:{art['genres']}­\n🗂Category:{art['type']}­\n❤️Popularity:{art['popularity']}­\n\n[IMAGE]({art['images'][0]['url']})\nArtist id:`{art['id']}`")
             except Exception as e:
                 pass
                 await message.reply(f"👤Artist: **{art['name']}­**\n❤️Followers:{art['followers']['total']}­\n🎶Generes:{art['genres']}­\n🗂Category:{art['type']}­\n❤️Popularity:{art['popularity']}­\n\n[IMAGE]({art['images'][0]['url']})\nArtist id:`{art['id']}`")     
             
             await message.reply(f"Sending Top 10 tracks of {art['name']}")
             tracks = client.artist_top_tracks(artist_id=item_id,)
             for item in tracks['tracks'][:10]:
                 song = await fetch_spotify_track(client,item.get('id'))
                 track = client.track(track_id=item['id'])
                 track_no = 1
                 try:
                     path = await download_songs(item,randomdir)
                 except Exception as e:
                     pass
                     await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
                     await message.reply(e)
                 thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                 audio = FLAC(path)
                 try:
                     audio["TITLE"] = f" {song.get('name')}"
                     audio["ORIGINALYEAR"] = song.get('year')
                     audio["YEAR_OF_RELEASE"] = song.get('year')
                     audio["WEBSITE"] = "https://t.me/spotify_downloa_bot"
                     audio["GEEK_SCORE"] = "9"
                     audio["ARTIST"] = art.get('name')                                                                            
                     audio["ALBUM"] = song.get('album')
                     audio["DATE"] = song.get('year')
                     audio["discnumber"] =f" {track['disc_number']}"
                     audio["tracknumber"] =f" {track['track_number']}"
                     try:
                         audio["ISRC"] =f" {track['external_ids']['isrc']}"
                     except:
                         pass
                     try:
                        songGenius = genius.search_song(song('name'), song('artist'))
                        audio["LYRICS"] = (songGenius.lyrics)
                     except:
                         pass
                 except:
                     pass
                 audio.save()
                 audi = File(path)
                 image = Picture() 
                 image.type = 3
                 if thumbnail.endswith('png'):
                    mime = 'image/png'
                 else:
                      mime = 'image/jpeg'
                 image.desc = 'front cover'
                 with open(thumbnail, 'rb') as f: # better than open(albumart, 'rb').read() ?
                     image.data = f.read()
 
                 audi.add_picture(image)
                 audi.save()
                 try:
                     await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                     AForCopy = await message.reply_audio(path,performer=f"{song.get('artist')}­",title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail, parse_mode=enums.ParseMode.MARKDOWN,quote=True,
                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
                 except:
                     pass
                 if LOG_GROUP:
                    await forward(PForCopy,AForCopy)
    except MissingSchema:
        pass
        await message.reply("400: Are You Sure It's valid URL🤨?")
    except RPCError:
        pass
        await message.reply(f"500: telegram says 500 error,so please try again later.❣️")
    except ChatWriteForbidden:
        pass
        chat=message.chat.id
        try:
            await Dxbotz.leave_chat(chat)
            k = await Dxbotz.send_message(-1001744816254,f"{chat} {message.chat.username} or {message.from_user.id}")
            await  k.pin()
            sp = f"I have left from {chat} reason: I Am Not  Admin "
            await Mbot.send_message(message.from_user.id,f"{sp}")
        except:
            pass
    except UserIsBlocked:
        pass
        K = await  Dxbotz.send_message(BUG,f" private {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
        k.pin()
    except IOError:
        pass
        K = await  Dxbotz.send_message(BUG,f" Private r: socket {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
        k.pin()
    except (FileNotFoundError, OSError):
        pass
        await message.reply('Sorry, We Are Unable To Procced It 🤕❣️')
    except BrokenPipeError:
        pass
        K = await  Dxbotz.send_message(BUG,f" private r: broken {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
    except Forbidden:
       T = await message.reply_text(f"Dude check weather I have enough rights😎⚠️")
    except UnboundLocalError:
       pass      
    except FloodWait as e:
        pass
        await sleep(e.value)
        await message.reply_text(f"420: Telegram says: [420 FLOOD_WAIT_X] - A wait of {e.value} seconds is required !")
    except SlowmodeWait:
       pass
       await sleep(e.value)
    except IOError as e:
        pass
        K = await  Dxbotz.send_message(BUG,f" private r: broken {message.chat.id} {message.from_user.mention}")
           
    except Exception as e:
        pass
        LOGGER.error(e)
        await m.edit(e)
        await Dxbotz.send_message(BUG,f" Finnal pv {e}")
        await message.reply('503: Sorry, We Are Unable To Procced It 🤕❣️')
    finally:
        await sleep(2.0)
        try:
            rmtree(randomdir)
        except:
            pass
        try:
            await message.reply_text(f"Done✅",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
            await message.reply_text(f"𝑪𝒉𝒆𝒄𝒌 𝑶𝒖𝒕 𝑴𝒚 𝑺𝒑𝒐𝒕𝒊𝒇𝒚 <a href=https://spotify.link/Zsi3FvqlLCb>Harsh Jha>.<</a>")
            await m.delete()
        except:
            pass 
           
@Dxbotz.on_callback_query(filters.regex(r"feed"))
async def feedback(Dxbotz,query):
      try:
          K = await query.message.edit(f"Feedback 🏴‍☠️",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Press here", url="https://t.me/makimamusic_support")]]))
          H = print("New Feedback")
          if BUG:
             await copy(K,H)
      except Exception as e:
          pass
         
@Dxbotz.on_callback_query(filters.regex(r"bug"))                                                                                                          
async def bug(_,query):
      try:                                                                                                                                  
          K = await query.message.edit(f'please report to the dev say "private version" with above  error occurred message')
          await sleep(2.3)
          H = await query.message.edit(f"Bug Report 🪲",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Report to dev ", url="https://t.me/masterolic")]]))
          if BUG:
             await copy(K,H)
      except Exception as e:
          pass
          print(e)

@Dxbotz.on_callback_query(filters.regex(r"cancel"))                                                                                                          
async def bug(_,query):
          await sleep(0.2)
          await query.message.delete()
          await query.answer("closed❌")
