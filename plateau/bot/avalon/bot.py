import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from const import ROLES, CHIPS, STATUS, EMOJI_PREFIX
from data import emojis
from util import reply_message, button_message, button_response, decompress_message
from service import component_response


load_dotenv(verbose=True)

bot = commands.Bot(command_prefix="=")
http = bot.http

# 이모지 참조를 위한 기본 경로
emoji_path = "./bot/avalon/emojis/"


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
        for chip in CHIPS:
            emoji = discord.utils.get(guild.emojis, name=chip)
            if emoji:
                guild_emojis[chip] = emoji.id

        emojis[guild.id] = guild_emojis
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 이모지 로딩 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="게임"))   # 온라인


@bot.command(aliases=["?", "명령", "아발론"])
async def avalon(msg: discord.Message):
    # 전체 command 리스트를 표시
    await button_message(msg, http, None, None, STATUS["COMMANDS"])


@bot.command(aliases=["설정", "이모지"])
async def emoticon(msg: discord.Message):
    emoji_list = os.listdir(emoji_path)
    for emoji_file in emoji_list:
        emoji = discord.utils.get(msg.guild.emojis, name=emoji_file.replace(".png", ''))
        if not emoji:
            with open(''.join([emoji_path, emoji_file]), 'rb') as fd:
                emoji = await msg.guild.create_custom_emoji(name=emoji_file.replace(".png", ''), image=fd.read())
                emojis[msg.guild.id][emoji_file.replace(".png", '')] = emoji.id
    await reply_message(msg, "아발론을 위한 이모지가 서버에 등록 되었습니다.")


@bot.event
async def on_socket_raw_receive(msg):
    msg = await decompress_message(msg)
    if msg["t"] == "INTERACTION_CREATE":
        datas = msg["d"]
        if datas["type"] == 3:
            if datas.get("message").get("type") == 0:
                msg = await bot.get_channel(int(datas["channel_id"])).fetch_message(int(datas["message"]["id"]))
            else:
                msg = await bot.get_channel(int(datas["channel_id"])).fetch_message(
                    int(datas["message"]["message_reference"]["message_id"]))
            user = await bot.fetch_user(datas.get("member").get("user")["id"])
            await button_response(msg, http, datas, user, component_response(datas))
    elif msg["t"] == "MESSAGE_REACTION_ADD":
        return
    elif msg["t"] == "MESSAGE_REACTION_REMOVE":
        return


@bot.event
async def on_command_error(msg, error):
    if isinstance(error, commands.CommandNotFound):
        await reply_message(msg, f"{msg.message.content}는 존재하지 않는 명령어입니다.", discord.Colour.dark_red())
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await reply_message(msg, "메세지 발송 권한이 없습니다. 설정 > 개인정보 보호 및 보안 > 서버 멤버가 보내는 다이렉트 메세지 허용하기가 켜져있는지 확인해주세요.",
                            discord.Colour.dark_red())
        return
    elif isinstance(error, commands.CommandInvokeError):
        await reply_message(msg, "이모지 등록 권한이 없습니다. 서버 설정 > 역할 > 권한 > 이모티콘 및 스티커 관리가 켜져있는지 확인해주세요.",
                            discord.Colour.dark_red())
        return
    await reply_message(msg, "오류가 발생했습니다. 아발론 > 해산 버튼을 클릭하여 원정을 종료하세요.", discord.Colour.dark_red())
    print(f"inigame - {datetime.datetime.now()} : <Error> {msg.channel.id}, error: {error}")


bot.run(os.getenv("TOKEN"))
