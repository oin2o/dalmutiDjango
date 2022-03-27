import os
import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from const import ROLES, QUESTS, COMMANDS, EXPLAIN, EMOJI_PREFIX, CARD_PREFIX
from data import emojis, games, roles
from game import Game
from util import directmsg, message, is_open, get_emoji, get_explain, get_status

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
    # 모집 시작된 원정이 있는지 점검
    current_game = await is_open(msg, 1)
    if not current_game:
        return
    # 현재 원정 상태를 표시
    await message(msg, 'send', f"{msg.guild.name}원정대", get_status(msg, current_game, roles, emojis), discord.Colour.dark_blue(), None)


@bot.command()
async def 모집(msg: discord.Message):
    # 채널에 미리 시작된 원정이 있는 경우는 추가 모집하지 않음
    if msg.channel.id in games:
        await message(msg, 'reply', '', f"{msg.guild.name}/{msg.channel.name}에서 원정이 진행 중 입니다.", discord.Colour.dark_blue(), None)
        return
    # 원정 처리를 위한 게임 데이터 저장소 생성
    current_game = {'game': Game()}
    games[msg.channel.id] = current_game
    # 게임의 상태를 모집 상태로 변경
    current_game['game'].recruit(msg)
    await message(msg, 'send', "원정대 모집이 시작되었습니다!", "원정에 참여할 플레이어는 &참가를 입력하세요.", discord.Colour.dark_blue(), None)


@bot.command()
async def 참가(msg: discord.Message):
    # 참가 가능한 원정이 있는지 점검
    current_game = await is_open(msg, 3)
    if not current_game:
        return
    # 플레이어를 해당 원정에 참가시킴
    '''
    if player not in current_game.members:
        current_game.join_in(msg)
        await message(msg, 'send', '', f"{msg.message.author.name}님이 참가하였습니다. 현재 원정대 {len(current_game.members)}명", discord.Colour.dark_blue(), None)
    else:
        await message(msg, 'send', '', f"{msg.message.author.name}님은 이미 참가 중 입니다.", discord.Colour.dark_red(), None)
    '''
    # 테스트 종료시 삭제 필요
    current_game.join_in(msg)
    await message(msg, 'send', '', f"{msg.message.author.name}님이 참가하였습니다. 현재 원정대 {len(current_game.members)}명", discord.Colour.dark_blue(), None)


@bot.command()
async def 마감(msg: discord.Message):
    # 모집 마감 가능한 원정이 있는지 점검
    current_game = await is_open(msg, 3)
    if not current_game:
        return
    # 원정대가 5명 이상인 경우만 마감 가능
    if len(current_game.members) < 5:
        await message(msg, 'send', "", "5명 이상의 원정대원이 필요합니다.", discord.Colour.dark_red(), None)
        return
    # 원정 모집을 마감 처리
    current_game.lock()
    await message(msg, 'send', '', "원정 모집이 마감되었습니다.", discord.Colour.dark_blue(), None)


@bot.command()
async def 시작(msg: discord.Message):
    # 시작할 수 있는 원정이 있는지 점검
    current_game = await is_open(msg, 1)
    if not current_game:
        return
    if current_game.join:
        await message(msg, 'send', "", "원정대 모집 중에는 시작할 수 없습니다.", discord.Colour.dark_red(), None)
        return
    # 원정을 시작
    current_game.start()
    # 순서 할당 및 역할 할당, 역할에 따른 DM 발송
    await message(msg, 'send', "원정이 시작되었습니다!", "역할을 확인하고, 원정을 수행하세요.", discord.Colour.dark_blue(), None)


@bot.command()
async def 종료(msg: discord.Message):
    # 종료할 수 있는 원정이 있는지 점검
    current_game = await is_open(msg, 1)
    if not current_game:
        return
    if not current_game.start:
        await message(msg, 'send', "", "진행 중인 원정이 없습니다.", discord.Colour.dark_red(), None)
        return
    # 원정을 종료
    current_game.end()
    # 원정 결과 발송
    await message(msg, 'send', "원정이 종료되었습니다!", "다시 원정을 떠나려면 &시작을 입력하세요.", discord.Colour.dark_blue(), None)


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
