import discord
from discord.http import Route

from const import EMOJI_PREFIX, CARD_PREFIX
from data import games

# 파일 참조를 위한 기본 경로
file_path = './bot/avalon/images/'


async def directmsg(msg, http, embed):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
    # post 전달 데이터 payload
    payload = {
        "embed": embed.to_dict(),
    }
    await http.request(r, json=payload)


async def message(msg, scope, title, description, color, file):
    # 메시지 타입(scope) 및 file 처리 여부에 따른 메시지 전송
    if scope == 'reply':
        if file:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == 'dm':
        if file:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == 'send':
        if file:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color))


async def is_open(msg, step):
    # 명령 처리 전, 단계 처리 가능여부 처리를 위한 validation
    if step >= 1:
        if msg.channel.id not in games:
            await message(msg, 'send', "", "모집 중인 원정이 존재하지 않습니다.", discord.Colour.dark_red(), None)
            return
        else:
            current_game = games[msg.channel.id]['game']
            if step >= 2:
                if not current_game.join:
                    await message(msg, 'send', "", "원정 참가가 이미 마감 되었습니다.", discord.Colour.dark_red(), None)
                    return
                elif step >= 3:
                    if len(current_game.members) >= 10:
                        await message(msg, 'send', "", "제한 인원(10명)을 초과 하였습니다.", discord.Colour.dark_red(), None)
                        return
    return current_game


def get_emoji(msg, role_kr, roles, emojis):
    # 이모지 표기 문자열 추가(디스코드 서버에 파일명과 동일하게 추가 필요)
    return ''.join(["<:", roles[role_kr], ":", str(emojis[msg.guild.id][''.join([EMOJI_PREFIX, roles[role_kr]])]), ">"])


def get_explain(msg, roles, emojis):
    return '\n'.join([
        "‣ 멀린팀",
        ' '.join([get_emoji(msg, "멀린", roles, emojis), "멀린 : 모드레드를 제외한 악을 알고 있습니다."]),
        ' '.join([get_emoji(msg, "퍼시발", roles, emojis), "퍼시발 : 멀린/모르가나가 보이지만, 정체는 모릅니다."]),
        ' '.join(
            [get_emoji(msg, "선의 세력1", roles, emojis), get_emoji(msg, "선의 세력2", roles, emojis),
             get_emoji(msg, "선의 세력3", roles, emojis), get_emoji(msg, "선의 세력4", roles, emojis),
             get_emoji(msg, "선의 세력5", roles, emojis), "선의 세력 : 원정을 성공 시키십시오."]),
        "",
        "‣ 모드레드팀",
        ' '.join([get_emoji(msg, "모드레드", roles, emojis), "모드레드 : 멀린에게 정체가 보이지 않습니다."]),
        ' '.join([get_emoji(msg, "모르가나", roles, emojis), "모르가나 : 퍼시발에게 멀린으로 위장합니다."]),
        ' '.join([get_emoji(msg, "암살자", roles, emojis), "암살자 : 멀린을 암살할 수 있습니다."]),
        ' '.join([get_emoji(msg, "오베론", roles, emojis), "오베론 : 악의 하수인과 서로 정체를 모릅니다."]),
        ' '.join(
            [get_emoji(msg, "악의 하수인1", roles, emojis), get_emoji(msg, "악의 하수인2", roles, emojis),
             get_emoji(msg, "악의 하수인3", roles, emojis), "악의 하수인 : 원정을 실패 시키십시오."]),
        "",
        "‣ 제3세력",
        "▪️ 랜슬롯 : 선/악 모두 존재하며, 원정 중, 팀을 배신할 수 있습니다."
    ])


def get_status(msg, current_game, roles, emojis):
    name = []
    desc = []
    for member in current_game.members:
        name.append(member.name)
    desc.append(': '.join(["원정대", ','.join(name)]))
    loyal_emoji = []
    evil_emoji = []
    for role_kr in current_game.roles['loyal']:
        loyal_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    for role_kr in current_game.roles['evil']:
        evil_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    desc.append(': '.join(["선", ' '.join(loyal_emoji)]))
    desc.append(': '.join(["악", ' '.join(evil_emoji)]))
    desc.append(': '.join(["상태", "원정중" if current_game.start else "모집중" if current_game.join else "원정준비"]))

    return '\n'.join(desc)
