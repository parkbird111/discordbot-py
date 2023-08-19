import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from lxml import html

def get_maple_text(url):
    response = requests.get(url)

    hrefs = []
    if response.status_code == 200:
        tree = html.fromstring(response.content)

        xpath_list = [
            '/html/body/div[1]/section[2]/section/table/tbody/tr[1]/td[2]/a',
            '/html/body/div[1]/section[2]/section/table/tbody/tr[2]/td[2]/a',
            '/html/body/div[1]/section[2]/section/table/tbody/tr[3]/td[2]/a'
        ]

        for xpath in xpath_list:
            href = tree.xpath(xpath + '/@href')
            if href:
                hrefs.append(href[0])
            else:
                hrefs.append(None)
    return hrefs
    

TOKEN = 'MTEzMzk3MTM2MTIxMjE0MTY0OQ.GW7PZp.8eIby0gEEwgrpNWEVSUnH0eknt7KCxOC6ScHVU'
PREFIX = '!'
CHANNEL_ID = 1133932594354987052

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name}이 온라인입니다!')

@bot.event
async def on_message(message):
    if message.content.startswith('!캐시'):
        hrefs = get_maple_text('https://maple.gg/info/update/cash')

        if all(href is not None for href in hrefs):
            await message.channel.send("신규 3종 일반캐시 목록입니다.")
            for href in hrefs:
                await message.channel.send(href)
        else:
            await message.channel.send("데이터를 가져오지 못했습니다.")


    elif message.content.startswith('!스라벨'):
        hrefs = get_maple_text('https://maple.gg/info/update/cash/special')

        if all(href is not None for href in hrefs):
            await message.channel.send("신규 3종 스페셜라벨(스라벨) 목록입니다.")
            for href in hrefs:
                await message.channel.send(href)
        else:
            await message.channel.send("데이터를 가져오지 못했습니다.")

   
   
    elif message.content.startswith('!마라벨'):
        hrefs = get_maple_text('https://maple.gg/info/update/cash/master')

        if all(href is not None for href in hrefs):
            await message.channel.send("신규 3종 마스터라벨(마라벨) 목록입니다.")
            for href in hrefs:
                await message.channel.send(href)
        else:
            await message.channel.send("데이터를 가져오지 못했습니다.")        

    await bot.process_commands(message)

bot.run(TOKEN)
