import discord
from discord.http import Route

from service import recruit, apply, expedition, end, status, component_response
from const import STATUS, BUTTONS, INTERACTION_SCOPE, COMMANDS, EXPLAIN, EMOJI_PREFIX
from data import emojis, games, roles

# 파일 참조를 위한 기본 경로
file_path = './bot/avalon/images/'


async def directmsg(msg, http, title, description, color, components):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
    # post 전달 데이터 payload
    payload = {
        "embed": discord.Embed(title=title, description=description, color=color).to_dict(),
        "components": components
    }
    await http.request(r, json=payload)


async def interactmsg(http, datas, description, components, flags):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=datas.get("id"), interaction_token=datas.get("token"))
    # post 전달 데이터 payload
    payload = {
        "type": 4,
        "data": {
            "content": description,
            "components": components,
            "flags": flags
        }
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


async def button_message(msg, http, datas, result):
    if result == STATUS['COMMANDS']:
        components = [{"type": 1, "components": [BUTTONS[STATUS["AVALON"]]]}]
        await directmsg(msg, http, "", COMMANDS, discord.Colour.default(), components)
    elif result == STATUS['AVALON']:
        components = [{"type": 1, "components": [BUTTONS[STATUS["EXPLAIN"]], BUTTONS[STATUS["STATUS"]], BUTTONS[STATUS["RECRUIT_DISABLE"]] if msg.channel.id in games else BUTTONS[STATUS["RECRUIT"]], BUTTONS[STATUS["DISMISSION"]]]}]
        await interactmsg(http, datas, "아발론에 오신걸 환영합니다!", components, INTERACTION_SCOPE["개인"])
    elif result == STATUS['EXPLAIN']:
        await interactmsg(http, datas, '\n'.join([EXPLAIN, "", get_explain(msg, roles, emojis)]), None, INTERACTION_SCOPE["개인"])


async def button_response(msg, http, datas, result):
    if result == STATUS['AVALON']:
        await button_message(msg, http, datas, result)
    elif result == STATUS['EXPLAIN']:
        await button_message(msg, http, datas, result)
    elif result == STATUS['STATUS']:
        await button_message(msg, http, datas, result)


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
        name.append(member.author.name)
    desc.append(': '.join(["원정대", ','.join(name)]))
    loyal_emoji = []
    evil_emoji = []
    for role_kr in current_game.roles['loyal']:
        loyal_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    for role_kr in current_game.roles['evil']:
        evil_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    desc.append(': '.join(["선", ' '.join(loyal_emoji)]))
    desc.append(': '.join(["악", ' '.join(evil_emoji)]))
    desc.append(': '.join(["상태", "원정중" if current_game.expedition else "모집중"]))

    return '\n'.join(desc)
