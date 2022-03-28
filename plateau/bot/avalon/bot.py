import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from const import ROLES, COMMANDS, EXPLAIN, EMOJI_PREFIX, CARD_PREFIX
from data import emojis, games, roles
from service import recruit, apply, expedition, end, status
from util import directmsg, message, status_message, get_explain

load_dotenv(verbose=True)

bot = commands.Bot(command_prefix='?')
http = bot.http


@bot.event
async def on_ready():
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 연결 시작")
    # 해당 봇이 포함된 전체 서버의 custom emoji id를 저장
    for guild in bot.guilds:
        guild_emojis = {}
        for role, role_kr in ROLES.items():
            roles[role_kr] = role
            emojiname = ''.join([EMOJI_PREFIX, role])
            emoji = discord.utils.get(guild.emojis, name=emojiname)
            if emoji:
                guild_emojis[emojiname] = emoji.id
        emojis[guild.id] = guild_emojis
    print(f"현재시각={datetime.datetime.now()}, 봇={bot.user.name} 이모지 로딩 완료")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="게임"))   # 온라인


@bot.command()
async def 명령(msg: discord.Message):
    # 전체 command 리스트를 표시
    await message(msg, 'reply', '', COMMANDS, discord.Colour.default(), None)


@bot.command()
async def 설명(msg: discord.Message):
    # 요청 유저에게 DM으로 설명 전송
    await message(msg, 'dm', '', '\n'.join([EXPLAIN, "", get_explain(msg, roles, emojis)]), discord.Colour.default(), None)
    await message(msg, 'reply', '', f"{msg.author.name}님에게 메세지를 발송하였습니다.", discord.Colour.default(), None)


@bot.command()
async def 상태(msg: discord.Message):
    await status_message(msg, status(msg, games))


@bot.command()
async def 모집(msg: discord.Message):
    await status_message(msg, recruit(msg, games))


@bot.command()
async def 참가(msg: discord.Message):
    await status_message(msg, apply(msg, games))


@bot.command()
async def 시작(msg: discord.Message):
    await status_message(msg, expedition(msg, games))


@bot.command()
async def 종료(msg: discord.Message):
    await status_message(msg, end(msg, games))


@bot.command()
async def 테스트(msg: discord.Message):
    await message(msg, 'dm', '', '\n'.join([EXPLAIN, "", get_explain(msg, roles, emojis)]), discord.Colour.default(), ''.join([CARD_PREFIX, "servant5.png"]))
    await directmsg(msg, http, discord.Embed(description=COMMANDS, colour=discord.Colour.default()))


@bot.event
async def on_command_error(msg, error):
    if isinstance(error, commands.CommandNotFound):
        await message(msg, 'reply', '', f"{msg.message.content} 는 존재하지 않는 명령어입니다.", discord.Colour.dark_red(), None)
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await message(msg, 'reply', '', "메세지 발송 권한이 없습니다. 설정 > 개인정보 보호 및 보안 > 서버 멤버가 보내는 다이렉트 메세지 허용하기 가 켜져있는지 확인해주세요.", discord.Colour.dark_red(), None)
        return
    await message(msg, 'reply', '', "오류가 발생했습니다. &종료를 통해 원정을 종료하세요.", discord.Colour.dark_red(), None)
    print(f"inigame - {datetime.datetime.now()} : <Error> {msg.channel.id}, error: {error}")


bot.run(os.getenv('TOKEN'))
