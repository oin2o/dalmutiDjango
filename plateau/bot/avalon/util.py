import zlib
import json

import discord
from discord.http import Route

from service import status, recruit, dismission, apply, psercival_morgana, modred, oberon, anonymous, commence, initial
from const import STATUS, BUTTONS, INTERACTION_SCOPE, INTERACTION_CALLBACK
from const import COMMANDS, AVALONS, EXPLAIN, RECRUITS, OPTIONS
from data import games
from strutil import get_explain, get_status

# 파일 참조를 위한 기본 경로
file_path = "./bot/avalon/images/"
# 압축 처리를 위한 zlib 객체
_zlib = zlib.decompressobj()


async def direct_message(msg, http, description, color=discord.Colour.default(), components=None, title=""):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route("POST", "/channels/{channel_id}/messages", channel_id=msg.channel.id)
    # post 전달 데이터 payload
    payload = {
        "embed": discord.Embed(title=title, description=description, color=color).to_dict(),
        "components": components,
    }
    await http.request(r, json=payload)


async def interact_message(msg, http, datas, description, color=discord.Colour.default(), components=None, title="",
                           flags=INTERACTION_SCOPE["개인"], callback=INTERACTION_CALLBACK["응답"]):
    # http 직접 메시지 전송을 위한 route 설정
    r = Route("POST", "/interactions/{interaction_id}/{interaction_token}/callback", interaction_id=datas.get("id"),
              interaction_token=datas.get("token"))
    # post 전달 데이터 payload
    if callback == INTERACTION_CALLBACK["ACK"]:
        payload = {
            "type": INTERACTION_CALLBACK["ACK"],
        }
        await direct_message(msg, http, description, color, components, title)
    else:
        payload = {
            "type": callback,
            "data": {
                "embeds": [discord.Embed(title=title, description=description, color=color).to_dict()],
                "components": components,
                "flags": flags
            }
        }
    await http.request(r, json=payload)


async def message(msg, scope, description, color=discord.Colour.default(), file=None, title=''):
    # 메시지 타입(scope) 및 file 처리 여부에 따른 메시지 전송
    if scope == "reply":
        if file:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.reply(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == "dm":
        if file:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.author.send(embed=discord.Embed(title=title, description=description, color=color))
    elif scope == "send":
        if file:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
                url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
        else:
            await msg.channel.send(embed=discord.Embed(title=title, description=description, color=color))


async def button_message(msg, http, datas, result):
    if result == STATUS["COMMANDS"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["AVALON"]]]}]
        await direct_message(msg, http, COMMANDS, discord.Colour.default(), components)
    elif result == STATUS["AVALON"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["EXPLAIN"]], BUTTONS[STATUS["STATUS"]],
                                                 BUTTONS[STATUS["RECRUIT"]], BUTTONS[STATUS["DISMISSION"]]]}]
        await interact_message(msg, http, datas, AVALONS, discord.Colour.default(), components, "아발론에 오신걸 환영합니다!")
    elif result == STATUS["EXPLAIN"]:
        await interact_message(msg, http, datas, '\n'.join([EXPLAIN, "", get_explain(msg)]))
    elif result == STATUS["STATUS"]:
        await interact_message(msg, http, datas, get_status(msg, games[msg.channel.id]["game"]),
                               discord.Colour.default(), None, "", INTERACTION_SCOPE["공개"])
    elif result == STATUS["RECRUIT"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["APPLY"]], BUTTONS[STATUS["OPTION"]],
                                                 BUTTONS[STATUS["COMMENCE"]], BUTTONS[STATUS["INITIAL"]]]}]
        await interact_message(msg, http, datas, RECRUITS, discord.Colour.default(), components, "원정을 준비하세요!",
                               INTERACTION_SCOPE["개인"], INTERACTION_CALLBACK["ACK"])
    elif result == STATUS["DISMISSION"]:
        await interact_message(msg, http, datas, "모집된 원정이 해산되었습니다.", discord.Colour.dark_red(), None, "",
                               INTERACTION_SCOPE["공개"])
    elif result == STATUS["APPLY"]:
        await interact_message(msg, http, datas, '\n'.join(["원정대에 참가하였습니다.", get_status(
            msg, games[msg.channel.id]["game"])]))
    elif result == STATUS["NO_RECRUIT"]:
        await interact_message(msg, http, datas, "모집(진행) 중인 원정이 존재하지 않습니다.", discord.Colour.dark_red())
    elif result == STATUS["NO_GAME"]:
        await interact_message(msg, http, datas, "원정이 존재하지 않습니다.", discord.Colour.dark_red())
    elif result == STATUS["ALREADY_START"]:
        await interact_message(msg, http, datas, "원정이 이미 시작되었습니다.", discord.Colour.dark_red())
    elif result == STATUS["MAX_MEMBER"]:
        await interact_message(msg, http, datas, "제한 인원(10명)을 초과하였습니다.", discord.Colour.dark_red())
    elif result == STATUS["MIN_MEMBER"]:
        await interact_message(msg, http, datas, "최소 인원(5명)이 모자랍니다.", discord.Colour.dark_red())
    elif result == STATUS["APPLY_CANCEL"]:
        await interact_message(msg, http, datas, "원정대 참가를 취소하였습니다.", discord.Colour.dark_red())
    elif result == STATUS["OPTION"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["PERCIVAL_MORGANA"]], BUTTONS[STATUS["MORDRED"]],
                                                 BUTTONS[STATUS["OBERON"]], BUTTONS[STATUS["ANONYMOUS"]]]}]
        await interact_message(msg, http, datas, OPTIONS, discord.Colour.default(), components, "")
    elif result == STATUS["COMMENCE"]:
        await interact_message(msg, http, datas, "역할을 확인하고, 원정을 수행하세요.", discord.Colour.dark_blue(), None,
                               "원정이 시작되었습니다!")
    elif result == STATUS["INITIAL"]:
        await interact_message(msg, http, datas, "새로운 원정을 준비하세요.", discord.Colour.dark_red(), None, "원정이 초기화되었습니다!")


async def button_response(msg, http, datas, user, result):
    if result == STATUS["STATUS"]:
        result = status(msg, games)
    elif result == STATUS["RECRUIT"]:
        result = recruit(msg, games, user)
    elif result == STATUS["DISMISSION"]:
        result = dismission(msg, games)
    elif result == STATUS["APPLY"]:
        result = apply(msg, games, user)
    elif result == STATUS["PERCIVAL_MORGANA"]:
        result = psercival_morgana(msg, games)
    elif result == STATUS["MORDRED"]:
        result = modred(msg, games)
    elif result == STATUS["OBERON"]:
        result = oberon(msg, games)
    elif result == STATUS["ANONYMOUS"]:
        result = anonymous(msg, games)
    elif result == STATUS["COMMENCE"]:
        result = commence(msg, games)
    elif result == STATUS["INITIAL"]:
        result = initial(msg, games)

    await button_message(msg, http, datas, result)


async def decompress_message(msg):
    _buffer = bytearray()
    if type(msg) is bytes:
        _buffer.extend(msg)
        if len(msg) < 4 or msg[-4:] != b"\x00\x00\xff\xff":
            return
        msg = _zlib.decompress(_buffer)
        return json.loads(msg.decode("utf-8"))
