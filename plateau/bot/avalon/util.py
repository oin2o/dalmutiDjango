import zlib
import json

import discord
from discord.http import Route

from service import status, recruit, dismission, apply, expedition, end, component_response
from const import STATUS, BUTTONS, INTERACTION_SCOPE, INTERACTION_CALLBACK, ROLES_REVERSE, COMMANDS, EXPLAIN, EMOJI_PREFIX
from data import emojis, games
from strutil import get_emoji, get_explain, get_status

# 파일 참조를 위한 기본 경로
file_path = './bot/avalon/images/'
# 압축 처리를 위한 zlib 객체
_zlib = zlib.decompressobj()


async def directmsg(msg, http, title, description, color, components):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
    # post 전달 데이터 payload
    payload = {
        "embed": discord.Embed(title=title, description=description, color=color).to_dict(),
        "components": components,
    }
    await http.request(r, json=payload)


async def interactmsg(msg, http, datas, callback, title, description, color, components, flags):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route('POST', '/interactions/{interaction_id}/{interaction_token}/callback', interaction_id=datas.get("id"),
              interaction_token=datas.get("token"))
    # post 전달 데이터 payload
    if callback == INTERACTION_CALLBACK["ACK"]:
        payload = {
            "type": INTERACTION_CALLBACK["ACK"],
        }
        await directmsg(msg, http, title, description, discord.Colour.dark_blue(), components)
    else:
        payload = {
            "type": callback,
            "data": {
                "embeds": [discord.Embed(title=title, description=description, color=color).to_dict()],
                "components": components,
                'message_id': msg.id,
                "flags": flags
            }
        }
    await http.request(r, json=payload)


async def message(msg, scope, title, description, color, file):
    # 메시지 타입(scope) 및 file 처리 여부에 따른 메시지 전송
    if scope == 'reply':
        if file:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == 'dm':
        if file:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == 'send':
        if file:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(['attachment://', file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color))


async def button_message(msg, http, datas, result):
    if result == STATUS['COMMANDS']:
        components = [{"type": 1, "components": [BUTTONS[STATUS["AVALON"]]]}]
        await directmsg(msg, http, "", COMMANDS, discord.Colour.default(), components)
    elif result == STATUS['AVALON']:
        components = [{"type": 1, "components": [BUTTONS[STATUS["EXPLAIN"]], BUTTONS[STATUS["STATUS"]],
                                                 BUTTONS[STATUS["RECRUIT"]], BUTTONS[STATUS["DISMISSION"]]]}]
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "아발론에 오신걸 환영합니다!", discord.Colour.default(), components, INTERACTION_SCOPE["개인"])
    elif result == STATUS['EXPLAIN']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", '\n'.join([EXPLAIN, "", get_explain(msg, ROLES_REVERSE, emojis)]), discord.Colour.default(), None,
                          INTERACTION_SCOPE["개인"])
    elif result == STATUS['STATUS']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", get_status(msg, games[msg.channel.id]['game'], ROLES_REVERSE, emojis), discord.Colour.default(), None,
                          INTERACTION_SCOPE["공개"])
    elif result == STATUS['RECRUIT']:
        components = [{"type": 1, "components": [BUTTONS[STATUS["APPLY"]], BUTTONS[STATUS["OPTION"]],
                                                 BUTTONS[STATUS["COMMENCE"]], BUTTONS[STATUS["INITIAL"]]]}]
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["ACK"], "", "원정을 준비하세요!", discord.Colour.default(), components, INTERACTION_SCOPE["개인"])
    elif result == STATUS['DISMISSION']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "모집된 원정이 해산되었습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["공개"])
    elif result == STATUS['APPLY']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", '\n'.join(["원정대에 참가하였습니다.", get_status(msg, games[msg.channel.id]['game'],
                                                                              ROLES_REVERSE, emojis)]), discord.Colour.default(), None,
                          INTERACTION_SCOPE["개인"])
    elif result == STATUS['NO_RECRUIT']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "모집(진행) 중인 원정이 존재하지 않습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["개인"])
    elif result == STATUS['NO_GAME']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "원정이 존재하지 않습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["개인"])
    elif result == STATUS['ALREADY_START']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "원정이 이미 시작되었습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["개인"])
    elif result == STATUS['MAX_MEMBER']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "제한 인원(10명)을 초과 하였습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["개인"])
    elif result == STATUS['APPLY_CANCEL']:
        await interactmsg(msg, http, datas, INTERACTION_CALLBACK["응답"], "", "원정대 참가를 취소하였습니다.", discord.Colour.default(), None, INTERACTION_SCOPE["개인"])


async def button_response(msg, http, datas, result):
    if result == STATUS['STATUS']:
        result = status(msg, games)
    elif result == STATUS['RECRUIT']:
        result = recruit(msg, games, datas.get("member").get("user"))
    elif result == STATUS['DISMISSION']:
        result = dismission(msg, games)
    elif result == STATUS['APPLY']:
        result = apply(msg, games, datas.get("member").get("user"))

    await button_message(msg, http, datas, result)


async def decompress_message(msg):
    _buffer = bytearray()
    if type(msg) is bytes:
        _buffer.extend(msg)
        if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
            return
        msg = _zlib.decompress(_buffer)
        return json.loads(msg.decode('utf-8'))
