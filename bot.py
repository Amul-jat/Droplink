from os import environ
import os
import time
from urllib.parse import urlparse
import aiohttp
from pyshorteners import Shortener
from bs4 import BeautifulSoup
import requests
import re
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')
CHANNEL = environ.get('CHANNEL')
HOWTO = environ.get('HOWTO')


bot = Client('Droplink bot', 
             api_id=API_ID, 
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm Droplink bot. Just send me link and get short link")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Pdisk Links, texts & images... Than I'll convert & replace all pdisk links with your pdisk links \nMessage me @kamdev07 For more help-**")

@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @kamdev07 or for more join @pdisk_Admins**")
    
@bot.on_message(filters.text & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{pdisk_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        if(len(pdisk_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{pdisk_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{pdisk_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
    
async def pdisk_up(link):
    if ('pdisk' in link or 'kuklink' in link or 'kofilink' in link or 'cofilink' in link or 'bit' in link or 'vdshort' in link or 'vidrivers' in link or 'dplinks' in link or 'wslinker' in link or 'cdinks' in link or 'dropxer' in link or 'droppx' in link):
        url = 'https://droplink.co/api'
        params = {'api': API_KEY, 'url': link}
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True) as response:
                data = await response.json()
                v_url =  data["shortenedUrl"]
    else:
        v_url = link
        
    return (v_url)

async def multi_pdisk_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = [sub.replace('https://t.me/Desi_Bhabhi_Aunty_hot_Video/41', 'https://t.me/Desi_Bhabhi_Aunty_hot_Video/61') for sub in new_ml_string]
    #new_ml_string = await remove_footer(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_pdisk_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    #return await addFooter(new_string)
    return (new_string)

async def new_pdisk_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await pdisk_up(i))
    return new_urls  

'''async def remove_footer(new_List):
    for i in new_List:
        if('https://t.me/Desi_Bhabhi_Aunty_hot_Video/41' in i):
            i = i.replace("41","61")
            #new_List.remove(i)
    return new_List'''
  
'''async def addFooter(str):
    footer = """
    ━━━━━━━━━━━━━━━
⚙️ How to Download / Watch Online :""" + HOWTO + """
━━━━━━━━━━━━━━━
⭐️JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer'''
        
bot.run()
