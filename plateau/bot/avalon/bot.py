import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from const import ROLES, CHIPS, STATUS, EMOJI_PREFIX
from data import emojis
from util import set_bot, send_message, button_message, button_response, message_delete, get_message, decompress_message
from service import component_response


load_dotenv(verbose=True)

bot = commands.Bot(command_prefix="=")
http = bot.http

# 이모지 참조를 위한 기본 경로
emoji_path = "./bot/avalon/emojis/"

# 메시지 삭제 기본 시간
delete_time = 3
# 메시지 대기 기본 시간
sleep_time = 30
# 삭제대상 메시지
delete_messages = []


@bot.event
async def on_ready():
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 연결 시작")
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 이모지 로딩 시작")
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
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 연결 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="=아발론"))   # 온라인
    # util에서 사용할 bot 객체 할당
    set_bot(bot)


@bot.event
async def on_message(message):
    if message.content.startswith('='):
        await bot.process_commands(message)
        await message_delete(message, delete_time)
        while delete_messages:
            await message_delete(delete_messages.pop(), sleep_time)


@bot.command(aliases=["?", "명령", "아발론"])
async def avalon(msg: discord.Message):
    # 전체 command 리스트를 표시
    await button_message(msg, http, None, None, STATUS["COMMANDS"])


@bot.command(aliases=["설정", "이모지"])
async def emoticon(msg: discord.Message):
    emoji_list = os.listdir(emoji_path)
    print(f"현재시각={datetime.datetime.now()}, 서버={msg.guild.name} 이모지 등록 시작")
    for emoji_file in emoji_list:
        emoji = discord.utils.get(msg.guild.emojis, name=emoji_file.replace(".png", ''))
        if not emoji:
            with open(''.join([emoji_path, emoji_file]), 'rb') as fd:
                emoji = await msg.guild.create_custom_emoji(name=emoji_file.replace(".png", ''), image=fd.read())
                emojis[msg.guild.id][emoji_file.replace(".png", '')] = emoji.id
    print(f"현재시각={datetime.datetime.now()}, 서버={msg.guild.name} 이모지 등록 완료")
    delete_messages.append(await send_message(msg, "아발론을 위한 이모지가 서버에 등록 되었습니다."))


@bot.event
async def on_socket_response(payload):
    if payload.get("t", "") == "INTERACTION_CREATE":
        datas = payload.get("d", {})
        if datas["type"] == 3:
            if datas.get("message").get("type") == 0:
                msg = await get_message(int(datas["channel_id"]), int(datas["message"]["id"]))
            else:
                msg = await get_message(int(datas["channel_id"]),
                                        int(datas["message"]["message_reference"]["message_id"]))
            await button_response(msg, http, datas, await bot.fetch_user(datas.get("member").get("user")["id"]),
                                  component_response(datas))


'''
@bot.event
async def on_socket_raw_receive(msg):
    msg = await decompress_message(msg)
    if msg["t"] == "INTERACTION_CREATE":
        datas = msg["d"]
        if datas["type"] == 3:
            if datas.get("message").get("type") == 0:
                msg = await get_message(int(datas["channel_id"]), int(datas["message"]["id"]))
            else:
                msg = await get_message(int(datas["channel_id"]),
                                        int(datas["message"]["message_reference"]["message_id"]))
            await button_response(msg, http, datas, await bot.fetch_user(datas.get("member").get("user")["id"]),
                                  component_response(datas))
'''


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await message_delete(
            await send_message(ctx, f"{ctx.message.content}는 존재하지 않는 명령어입니다.", discord.Colour.dark_red()),
            sleep_time)
    elif isinstance(error, commands.BotMissingPermissions):
        await message_delete(
            await send_message(ctx, "메세지 발송 권한이 없습니다. 설정 > 개인정보 보호 및 보안 > 서버 멤버가 보내는 다이렉트 메세지 허용하기가 켜져있는지 확인해주세요.",
                               discord.Colour.dark_red()),
            sleep_time)
    elif isinstance(error, commands.CommandInvokeError):
        await message_delete(
            await send_message(ctx, "권한 혹은 명령 오류가 발생했습니다. 관리자에게 문의해 주세요.", discord.Colour.dark_red()),
            sleep_time)
    else:
        await message_delete(
            await send_message(ctx, "오류가 발생했습니다. 아발론 > 해산 버튼을 클릭하여 원정을 종료하세요.", discord.Colour.dark_red()),
            sleep_time)
    print(f"inigame - {datetime.datetime.now()} : <Error> {ctx.channel.id}, error: {error}")


bot.run(os.getenv("TOKEN"))
