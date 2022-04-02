import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from const import ROLES, STATUS, EMOJI_PREFIX
from data import emojis
from util import message, button_message, button_response, decompress_message
from service import component_response


load_dotenv(verbose=True)

bot = commands.Bot(command_prefix='=')
http = bot.http


@bot.event
async def on_ready():
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 연결 시작")
    # 해당 봇이 포함된 전체 서버의 custom emoji id를 저장
    for guild in bot.guilds:
        guild_emojis = {}
        for role, role_kr in ROLES.items():
            emojiname = ''.join([EMOJI_PREFIX, role])
            emoji = discord.utils.get(guild.emojis, name=emojiname)
            if emoji:
                guild_emojis[emojiname] = emoji.id
        emojis[guild.id] = guild_emojis
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 이모지 로딩 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="게임"))   # 온라인


@bot.command(aliases=["?"])
async def 명령(msg: discord.Message):
    # 전체 command 리스트를 표시
    await button_message(msg, http, None, STATUS['COMMANDS'])


@bot.command()
async def 설정(msg: discord.Message):
    await button_message(msg, http, None, STATUS['AVALON'])


'''
@bot.event
async def on_socket_response(payload):
    t = payload.get("t")
    if t == "INTERACTION_CREATE":
        datas = payload.get("d", {})
        if datas.get("type") == 3:
            if datas.get('message').get('type') == 0:
                msg = await bot.get_channel(int(datas.get('channel_id'))).fetch_message(int(datas.get('message').get('id')))
            else:
                msg = await bot.get_channel(int(datas.get('channel_id'))).fetch_message(int(datas.get('message').get(
                    'message_reference').get('message_id')))
            await button_response(msg, http, datas, component_response(datas))
'''


@bot.event
async def on_socket_raw_receive(msg):
    msg = await decompress_message(msg)
    if msg["t"] == "INTERACTION_CREATE":
        datas = msg["d"]
        if datas["type"] == 3:
            if datas.get('message').get('type') == 0:
                msg = await bot.get_channel(int(datas["channel_id"])).fetch_message(int(datas["message"]["id"]))
            else:
                msg = await bot.get_channel(int(datas["channel_id"])).fetch_message(
                    int(datas["message"]["message_reference"]["message_id"]))
            await button_response(msg, http, datas, component_response(datas))


@bot.event
async def on_command_error(msg, error):
    if isinstance(error, commands.CommandNotFound):
        await message(msg, 'reply', '', f"{msg.message.content} 는 존재하지 않는 명령어입니다.", discord.Colour.dark_red(), None)
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await message(msg, 'reply', '', "메세지 발송 권한이 없습니다. 설정 > 개인정보 보호 및 보안 > 서버 멤버가 보내는 다이렉트 메세지 허용하기가 켜져있는지 확인해주세요.",
                      discord.Colour.dark_red(), None)
        return
    await message(msg, 'reply', '', "오류가 발생했습니다. 아발론 > 해산 버튼을 클릭하여 원정을 종료하세요.", discord.Colour.dark_red(), None)
    print(f"inigame - {datetime.datetime.now()} : <Error> {msg.channel.id}, error: {error}")


bot.run(os.getenv('TOKEN'))
