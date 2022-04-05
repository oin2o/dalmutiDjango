import zlib
import json

import discord
from discord.http import Route

from service import status, recruit, dismission, apply, option, psercival_morgana, mordred, oberon, anonymous
from service import commence, initial, organize, proposal
from service import vote, check_vote, assassin, quest, check_quest, next_vote, viviane
from const import STATUS, BUTTONS, INTERACTION_SCOPE, INTERACTION_CALLBACK, ROLES_REVERSE, CARD_PREFIX
from const import ROLES, COMMANDS, AVALONS, EXPLAIN, RECRUITS, OPTIONS
from data import games
from strutil import get_explain, get_status, get_role

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
        if description:
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


async def reply_message(msg, description, color=discord.Colour.default(), file=None, title=''):
    # file 처리 여부에 따른 메시지 전송
    if file:
        return await msg.reply(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
            url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
    else:
        return await msg.reply(embed=discord.Embed(title=title, description=description, color=color))


async def dm_message(user, description, color=discord.Colour.default(), file=None, title=''):
    if file:
        await user.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
            url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
    else:
        await user.send(embed=discord.Embed(title=title, description=description, color=color))


async def send_message(msg, description, color=discord.Colour.default(), file=None, title=''):
    # file 처리 여부에 따른 메시지 전송
    if file:
        return await msg.send(embed=discord.Embed(title=title, description=description, color=color).set_thumbnail(
            url=''.join(["attachment://", file])), file=discord.File(''.join([file_path, file])) if file else None)
    else:
        return await msg.send(embed=discord.Embed(title=title, description=description, color=color))


async def button_message(msg, http, datas, user, result):
    if result == STATUS["COMMANDS"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["AVALON"]]]}]
        await direct_message(msg, http, COMMANDS, discord.Colour.default(), components)
    elif result == STATUS["AVALON"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["EXPLAIN"]], BUTTONS[STATUS["STATUS"]],
                                                 BUTTONS[STATUS["RECRUIT"]], BUTTONS[STATUS["DISMISSION"]]]}]
        await interact_message(msg, http, datas, AVALONS, discord.Colour.default(), components, "아발론에 오신걸 환영합니다!")
    elif result == STATUS["EXPLAIN"]:
        # await interact_message(msg, http, datas, '\n'.join([EXPLAIN, "", get_explain(msg)]))
        # 상호작용 종료를 위한 단순 ACK처리
        await interact_message(msg, http, datas, None, discord.Colour.default(), None, "", INTERACTION_SCOPE["개인"],
                               INTERACTION_CALLBACK["ACK"])
        await dm_message(user, '\n'.join([EXPLAIN, "", get_explain(msg)]), discord.Colour.dark_purple())
    elif result == STATUS["STATUS"]:
        await interact_message(msg, http, datas, get_status(msg, games[msg.channel.id]["game"]),
                               discord.Colour.default(), None, "", INTERACTION_SCOPE["공개"])
    elif result == STATUS["RECRUIT"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["APPLY"]], BUTTONS[STATUS["OPTION"]],
                                                 BUTTONS[STATUS["COMMENCE"]], BUTTONS[STATUS["INITIAL"]]]}]
        await interact_message(msg, http, datas, RECRUITS, discord.Colour.default(), components, "원정을 준비하세요!",
                               INTERACTION_SCOPE["개인"], INTERACTION_CALLBACK["ACK"])
        # 모집시에 아발론 명령어 메시지 삭제(설명 상태 모집 해산은 개인 상호작용 메시지라 삭제 안함)
        #await msg.delete()
    elif result == STATUS["DISMISSION"]:
        await interact_message(msg, http, datas, "모집된 원정이 해산되었습니다.", discord.Colour.dark_red(), None, "",
                               INTERACTION_SCOPE["공개"])
    elif result == STATUS["APPLY"]:
        await interact_message(msg, http, datas, '\n'.join(["원정대에 참가하였습니다.", get_status(
            msg, games[msg.channel.id]["game"])]))
    elif result == STATUS["NO_GAME"] or result == STATUS["NO_RECRUIT"] or result == STATUS["ALREADY_START"] \
            or result == STATUS["APPLY_CANCEL"] or result == STATUS["MAX_MEMBER"] or result == STATUS["MIN_MEMBER"]:
        await interact_message(msg, http, datas,
                               "원정이 존재하지 않습니다." if result == STATUS["NO_GAME"]
                               else "모집(진행) 중인 원정이 존재하지 않습니다." if result == STATUS["NO_RECRUIT"]
                               else "원정이 이미 시작되었습니다." if result == STATUS["ALREADY_START"]
                               else "원정대 참가를 취소하였습니다." if result == STATUS["APPLY_CANCEL"]
                               else "제한 인원(10명)을 초과하였습니다." if result == STATUS["MAX_MEMBER"]
                               else "최소 인원(5명)이 모자랍니다.", discord.Colour.dark_red())
    elif result == STATUS["OPTION"]:
        components = [{"type": 1, "components": [BUTTONS[STATUS["PERCIVAL_MORGANA"]], BUTTONS[STATUS["MORDRED"]],
                                                 BUTTONS[STATUS["OBERON"]], BUTTONS[STATUS["ANONYMOUS"]]]}]
        await interact_message(msg, http, datas, OPTIONS, discord.Colour.default(), components, "")
    elif result == STATUS["COMMENCE"]:
        await interact_message(msg, http, datas,
                               '\n'.join(["역할을 확인하고, 원정을 준비하세요.",
                                          ''.join([games[msg.channel.id]["game"].leader.user.name, "님이 현재 원정대장입니다."])]),
                               discord.Colour.dark_blue(), None, "원정이 시작되었습니다!", INTERACTION_SCOPE["공개"])
        # 개인메시지로 역할 및 직업 정보 보내기
        await game_message(msg, http, games[msg.channel.id]["game"], result)
        # 1라운드 원정대장에게 구성 메시지 발송
        await game_message(msg, http, games[msg.channel.id]["game"], STATUS["ORGANIZE"])
        # 시작시에 참가 옵션 시작 초기화 명령어 메시지 삭제
        await msg.delete()
    elif result == STATUS["INITIAL"]:
        await interact_message(msg, http, datas, "새로운 원정을 준비하세요.", discord.Colour.dark_red(), None, "원정이 초기화되었습니다!")
    elif result == STATUS["NO_PERMISSION"] or result == STATUS["NO_MEMBER"] \
            or result == STATUS["MAX_ORGANIZE"] or result == STATUS["MIN_ORGANIZE"]:
        await interact_message(msg, http, datas,
                               ''.join([datas.get("member").get("user")["username"], "님은 할 수 없는 동작입니다."])
                               if result == STATUS["NO_PERMISSION"]
                               else "선택한 멤버가 원정에 포함된 인원이 아닙니다." if result == STATUS["NO_MEMBER"]
                               else "원정대원을 모두 선택하셨습니다." if result == STATUS["MAX_ORGANIZE"]
                               else "원정대원이 모자랍니다.", discord.Colour.dark_red())
    elif result == STATUS["ORGANIZE"]:
        desc = [''.join(["‣ 원정구성(총 ", str(games[msg.channel.id]["game"].rounds[
                                              games[msg.channel.id]["game"].quest_round]["players"]), "명)"])]
        for member in games[msg.channel.id]["game"].rounds[games[msg.channel.id]["game"].quest_round]["members"]:
            desc.append(''.join(["••• ", member.user.name]))
        await interact_message(msg, http, datas, '\n'.join(desc), discord.Colour.dark_blue())
    elif result == STATUS["PROPOSAL"]:
        current_game = games[msg.channel.id]["game"]
        # 전체 멤버에게 투표 문자 보내기
        desc = ["원정대 구성에 대해 찬성/반대를 투표해주세요.", "‣ 원정구성"]
        for member in current_game.rounds[current_game.quest_round]["members"]:
            desc.append(''.join(["••• ", member.user.name]))
        components = [{"type": 1, "components": [BUTTONS[STATUS["APPROVE"]], BUTTONS[STATUS["REJECT"]]]}]
        await direct_message(msg, http, '\n'.join(desc), discord.Colour.dark_blue(), components,
                             ''.join([current_game.leader.user.name, "님이 ",
                                      str(current_game.quest_round), "라운드 ",
                                      str(current_game.rounds[current_game.quest_round]["deny"] + 1),
                                      "번째 원정대를 제안하였습니다."]))

        # 원정대 구성 메시지 삭제하기
        await msg.delete()
        '''
        reply_msg = await reply_message(msg, '\n'.join(desc), discord.Colour.default(), None,
                                        ''.join([current_game.leader.user.name, "님이 ",
                                                 str(current_game.quest_round), "라운드 ",
                                                 str(current_game.rounds[current_game.quest_round]["deny"] + 1),
                                                 "번째 원정대를 제안하였습니다."]))
        
        # 찬성/반대 이모지로 리액션 처리를 위한 객체 생성
        approve_emoji = discord.utils.get(msg.guild.emojis, name="avalon_chip_approve")
        reject_emoji = discord.utils.get(msg.guild.emojis, name="avalon_chip_reject")
        await reply_msg.add_reaction(approve_emoji)
        await reply_msg.add_reaction(reject_emoji)

        # 원정대 구성 메시지 삭제하기
        await msg.delete()
        # 리액션에 대해 일정시간(60초) 대기하며 처리
        try:
            reaction, reaction_user = await avalon_bot.wait_for('reaction_add', timeout=60)
            if reaction.emoji == approve_emoji:
                # 찬성버튼을 클릭한 경우, 현재 게임 라운드의 투표내용에 등록
                await direct_message(msg, http, "원정 구성을 찬성하였습니다.", discord.Colour.dark_blue())
            elif reaction.emoji == reject_emoji:
                await direct_message(msg, http, "원정 구성을 반대하였습니다.", discord.Colour.dark_red())
        except asyncio.TimeoutError:
            await direct_message(msg, http, "정해진 시간내 투표하지 않아 찬성처리 하였습니다.", discord.Colour.dark_red())
        '''
    elif result == STATUS["APPROVE"] or result == STATUS["REJECT"]:
        current_round = games[msg.channel.id]["game"].rounds[games[msg.channel.id]["game"].quest_round]
        total_vote = len(current_round["vote"]["approval"]) + len(current_round["vote"]["reject"])
        await interact_message(msg, http, datas, '\n'.join(["원정대 구성에 찬성하셨습니다." if result == STATUS["APPROVE"]
                                                            else "원정대 구성에 반대하셨습니다.",
                                                            ''.join(["현재까지 총 ",
                                                                     str(len(games[msg.channel.id]["game"].members)),
                                                                     "명 중 ", str(total_vote), "명이 투표했습니다."]),
                                                            "마지막 투표 결과만 반영됩니다."]),
                               discord.Colour.dark_blue() if result == STATUS["APPROVE"] else discord.Colour.dark_red())
        # 투표 후처리
        await button_message(msg, http, datas, user, check_vote(games[msg.channel.id]["game"]))
    elif result == STATUS["EXPEDITION_ROUND"]:
        # 라운드의 원정대원들에게 성공/실패 투표 REPLY 전송
        current_game = games[msg.channel.id]["game"]
        # 익명 여부에 따라 투표 결과 공개
        desc = ["‣ 투표결과"]
        if not current_game.anonymous:
            approve = []
            reject = []
            for member in current_game.members:
                if member in current_game.rounds[current_game.quest_round]["vote"]["approval"]:
                    approve.append(member.user.name)
                if member in current_game.rounds[current_game.quest_round]["vote"]["reject"]:
                    reject.append(member.user.name)
            desc.append(''.join(["••• 찬성(", str(len(current_game.rounds[current_game.quest_round]["vote"]["approval"])),
                                 "명) : ", ", ".join(approve)]))
            desc.append(''.join(["••• 반대(", str(len(current_game.rounds[current_game.quest_round]["vote"]["reject"])),
                                 "명) : ", ", ".join(reject)]))
        else:
            desc.append(''.join(["••• 찬성(", str(len(current_game.rounds[current_game.quest_round]["vote"]["approval"])),
                                 "명)"]))
            desc.append(''.join(["••• 반대(", str(len(current_game.rounds[current_game.quest_round]["vote"]["reject"])),
                                 "명)"]))
        # 라운드의 원정대원에게 투표 문자 보내기
        desc.append("‣ 원정구성")
        for member in current_game.rounds[current_game.quest_round]["members"]:
            desc.append(''.join(["••• ", member.user.name]))
        components = [{"type": 1, "components": [BUTTONS[STATUS["QUEST_SUCCESS"]], BUTTONS[STATUS["QUEST_FAIL"]]]}]
        await direct_message(msg, http, '\n'.join(desc), discord.Colour.dark_blue(), components,
                             ''.join([str(current_game.quest_round), "라운드 ",
                                      str(current_game.rounds[current_game.quest_round]["deny"] + 1),
                                      "번째 원정대의 결과를 선택해 주세요."]))
        # 찬성 반대 투표메시지 삭제하기
        await msg.delete()
    elif result == STATUS["LOYAL_FAIL"] or result == STATUS["ALREADY_RESULT"]:
        await interact_message(msg, http, datas,
                               "선의 세력은 성공만 투표 가능합니다." if result == STATUS["LOYAL_FAIL"]
                               else "이미 원정 결과를 제출했습니다.", discord.Colour.dark_red())
    elif result == STATUS["QUEST_SUCCESS"] or result == STATUS["QUEST_FAIL"]:
        await interact_message(msg, http, datas,
                               "원정 성공에 한표 제출하였습니다." if result == STATUS["QUEST_SUCCESS"]
                               else "원정 실패에 한 표 제출하였습니다.",
                               discord.Colour.dark_blue() if result == STATUS["QUEST_SUCCESS"]
                               else discord.Colour.dark_red())
        # 투표 후처리
        await button_message(msg, http, datas, user, check_quest(games[msg.channel.id]["game"]))
    elif result == STATUS["VIVIANE"]:
        # 호수의 여신(비비안)을 사용 전달
        await game_message(msg, http, games[msg.channel.id]["game"], STATUS["VIVIANE"])
        # 라운드 성공/실패 선택 후, 호수의 여신(비비안) 단계 진행시 이전 라운드 결과 메시지 삭제
        await msg.delete()
    elif result == STATUS["ORGANIZE_ROUND"]:
        # 부결결과 전송 및 다음 리더로 변경
        # 라운드의 원정대원들에게 성공/실패 투표 REPLY 전송
        current_game = games[msg.channel.id]["game"]
        # 익명 여부에 따라 투표 결과 공개
        desc = ["‣ 투표결과"]
        if not current_game.anonymous:
            approve = []
            reject = []
            for member in current_game.members:
                if member in current_game.rounds[current_game.quest_round]["vote"]["approval"]:
                    approve.append(member.user.name)
                if member in current_game.rounds[current_game.quest_round]["vote"]["reject"]:
                    reject.append(member.user.name)
            desc.append(''.join(["••• 찬성(", str(len(current_game.rounds[current_game.quest_round]["vote"]["approval"])),
                                 "명) : ", ", ".join(approve)]))
            desc.append(''.join(["••• 반대(", str(len(current_game.rounds[current_game.quest_round]["vote"]["reject"])),
                                 "명) : ", ", ".join(reject)]))
        else:
            desc.append(''.join(["••• 찬성(", str(len(current_game.rounds[current_game.quest_round]["vote"]["approval"])),
                                 "명)"]))
            desc.append(''.join(["••• 반대(", str(len(current_game.rounds[current_game.quest_round]["vote"]["reject"])),
                                 "명)"]))
        desc.append("다음 원정을 준비하세요.")
        desc.append(''.join([current_game.leader.user.name, "님이 현재 원정대장입니다."]))
        await direct_message(msg, http, '\n'.join(desc), discord.Colour.dark_blue(), None, "원정대 구성이 부결되었습니다!")
        # 원정대 라운드 구성/투표 초기화 및 원정대장 변경
        next_vote(current_game)
        # 원정대장에게 구성 메시지 발송
        await game_message(msg, http, current_game, STATUS["ORGANIZE"])
        # 찬성 반대 투표메시지 삭제하기
        await msg.delete()
    elif result == STATUS["ORGANIZE_QUEST"]:
        current_game = games[msg.channel.id]["game"]
        # 라운드에 맞는 실패 장수에 따라 실패여부 확인
        fail_count = len(current_game.rounds[current_game.quest_round - 1]["result"]["fail"])
        is_fail = False
        if fail_count > 0:
            if current_game.fourth_round and current_game.quest_round - 1 == 4:
                if fail_count >= 2:
                    is_fail = True
            else:
                is_fail = True
        desc = ''.join(["‣ 원정결과: ",
                        ''.join(["실패 ", str(fail_count), "장"]) if is_fail else ''.join(["성공(실패 ", str(fail_count), "장"])
                        if current_game.fourth_round and current_game.quest_round - 1 == 4 else "성공"])
        # 결과 전송 및 다음 리더로 변경
        await direct_message(msg, http, '\n'.join([desc, get_status(msg, current_game)]), discord.Colour.default(),
                             None, "원정대 원정 결과!")
        # 원정대장에게 구성 메시지 발송
        await game_message(msg, http, current_game, STATUS["ORGANIZE"])
        # 라운드 성공/실패 선택 후, 다음 라운드 진행 시 이전 라운드 결과 메시지 삭제
        await msg.delete()
    elif result == STATUS["TERMINATE_LOYAL"] or result == STATUS["TERMINATE_EVIL"]:
        # 선의 승리인 경우, 결과 공지 및 암살자에게 선택권 제공
        # 악의 승리인 경우, 결과 공지 및 종료
        await direct_message(msg, http, get_status(msg, games[msg.channel.id]["game"]),
                             discord.Colour.dark_blue() if result == STATUS["TERMINATE_LOYAL"]
                             else discord.Colour.dark_red(), None, "원정이 성공하였으나, 암살자를 조심하세요!"
                             if result == STATUS["TERMINATE_LOYAL"] else "악의 하수인들의 활약으로 원정이 실패하였습니다!")
        # 성공 종료인 경우, 암살자 선택권 출력
        if result == STATUS["TERMINATE_LOYAL"]:
            await game_message(msg, http, games[msg.channel.id]["game"], STATUS["ASSASSIN"])
        # 찬성 반대 투표메시지 삭제하기
        await msg.delete()
        # 실패 종료인 경우, 게임 초기화
        if result == STATUS["TERMINATE_EVIL"]:
            games[msg.channel.id]["game"].clear_game()
    elif result == STATUS["ASSASSIN"] or result == STATUS["ASSASSIN_FAIL"]:
        # 암살 결과 공지 및 종료
        await interact_message(msg, http, datas, get_status(msg, games[msg.channel.id]["game"]),
                               discord.Colour.dark_red() if result == STATUS["ASSASSIN"]
                               else discord.Colour.dark_blue(), None,
                               "암살이 성공하여 악의 하수인들이 승리하였습니다!" if result == STATUS["ASSASSIN"]
                               else "암살이 실패하여 아서왕의 수하들이 승리하였습니다!", INTERACTION_SCOPE["공개"])
        # 암살 메시지 삭제하기
        await msg.delete()
        # 게임 초기화
        games[msg.channel.id]["game"].clear_game()
    elif result == STATUS["VIVIANE_LOYAL"] or result == STATUS["VIVIANE_EVIL"]:
        # 상호작용 종료를 위한 단순 ACK처리
        await interact_message(msg, http, datas, None, discord.Colour.default(), None, "", INTERACTION_SCOPE["개인"],
                               INTERACTION_CALLBACK["ACK"])
        result_viviane = False
        # 개인메시지로 호수의 여신 결과 보내기
        if result == STATUS["VIVIANE_LOYAL"]:
            result_viviane = True
        await dm_message(user, ''.join([datas.get("data", {}).get("custom_id").split('_')[-1],
                                        "님은 아서왕의 충성스러운 수하입니다." if result_viviane else "님은 악의 하수인입니다."]),
                         discord.Colour.dark_blue() if result_viviane else discord.Colour.dark_red(),
                         ''.join([CARD_PREFIX, "viviane", ".png"]), "호수의 여신(비비안)!")
        # 호수의 여신 메시지 삭제하기
        await msg.delete()


async def button_response(msg, http, datas, user, result):
    if result == STATUS["STATUS"]:
        result = status(msg, games)
    elif result == STATUS["RECRUIT"]:
        result = recruit(msg, games, user)
    elif result == STATUS["DISMISSION"]:
        result = dismission(msg, games)
    elif result == STATUS["APPLY"]:
        result = apply(msg, games, user)
    elif result == STATUS["OPTION"]:
        result = option(msg, games)
    elif result == STATUS["PERCIVAL_MORGANA"]:
        result = psercival_morgana(msg, games)
    elif result == STATUS["MORDRED"]:
        result = mordred(msg, games)
    elif result == STATUS["OBERON"]:
        result = oberon(msg, games)
    elif result == STATUS["ANONYMOUS"]:
        result = anonymous(msg, games)
    elif result == STATUS["COMMENCE"]:
        result = commence(msg, games)
    elif result == STATUS["INITIAL"]:
        result = initial(msg, games)
    elif result == STATUS["ORGANIZE"]:
        result = organize(msg, games, datas, user)
    elif result == STATUS["PROPOSAL"]:
        result = proposal(msg, games, user)
    elif result == STATUS["APPROVE"]:
        result = vote(msg, games, user, True)
    elif result == STATUS["REJECT"]:
        result = vote(msg, games, user, False)
    elif result == STATUS["ASSASSIN"]:
        result = assassin(msg, games, datas, user)
    elif result == STATUS["QUEST_SUCCESS"]:
        result = quest(msg, games, user, True)
    elif result == STATUS["QUEST_FAIL"]:
        result = quest(msg, games, user, False)
    elif result == STATUS["VIVIANE"]:
        result = viviane(msg, games, datas, user)

    await button_message(msg, http, datas, user, result)


async def decompress_message(msg):
    _buffer = bytearray()
    if type(msg) is bytes:
        _buffer.extend(msg)
        if len(msg) < 4 or msg[-4:] != b"\x00\x00\xff\xff":
            return
        msg = _zlib.decompress(_buffer)
        return json.loads(msg.decode("utf-8"))


async def game_message(msg, http, current_game, scope):
    if scope == STATUS["COMMENCE"]:
        # 게임 시작 시, 개인메시지로 역할 및 직업 정보 보내기
        for member in current_game.members:
            await dm_message(member.user, get_role(current_game, member),
                             discord.Colour.dark_blue() if member.role in current_game.roles["loyal"] else
                             discord.Colour.dark_red(),
                             ''.join([CARD_PREFIX, ROLES_REVERSE[member.role["name"]], ".png"]),
                             ''.join(["당신의 역할은 ", member.role["name"], "입니다."]))
    elif scope == STATUS["ORGANIZE"]:
        components = [{"type": 1, "components": []}]
        # 원정대 구성을 위해 전체 원정대원에 대한 버튼 컴포넌트 설정
        for member in current_game.members:
            components[-1]["components"].append({"type": 2, "label": member.user.name, "style": 3,
                                                "custom_id": '_'.join([STATUS["ORGANIZE"], member.user.name])})
            if len(components[-1]["components"]) > 0 and len(components[-1]["components"]) % 4 == 0:
                components.append({"type": 1, "components": []})
        # 버튼 설정 후, 제안 버튼 추가
        components[-1]["components"].append(BUTTONS[STATUS["PROPOSAL"]])
        # 원정대장에게 원정구성 DM 발송(DM에 버튼)
        # DM에 버튼 포함 이슈로 1차적으로 채널에 표기되도록 구현
        await direct_message(msg, http,
                             ''.join(["이번 라운드에 지목할 원정대원 수는 ",
                                      str(current_game.rounds[current_game.quest_round]["players"]), "명입니다."]),
                             discord.Colour.dark_blue(), components,
                             ''.join([current_game.leader.user.name, "님, 원정대를 구성해 주세요!"]))
    elif scope == STATUS["ASSASSIN"]:
        components = [{"type": 1, "components": []}]
        # 암살을 위해 악의 세력을 제외한 원정대원에 대한 버튼 컴포넌트 설정
        assassin_name = ""
        for member in current_game.members:
            if member.role == ROLES["assassin"]:
                assassin_name = member.user.name
            if member.role not in (ROLES["assassin"], ROLES["morgana"], ROLES["mordred"], ROLES["lancelot_evil"],
                                   ROLES["minion1"], ROLES["minion2"], ROLES["minion3"]):
                components[-1]["components"].append({"type": 2, "label": member.user.name, "style": 4,
                                                     "custom_id": '_'.join([STATUS["ASSASSIN"], member.user.name])})
            if len(components[-1]["components"]) > 0 and len(components[-1]["components"]) % 4 == 0:
                components.append({"type": 1, "components": []})
        # 마지막 ROW의 컴포넌트 값이 없는 경우 제외
        if len(components[-1]["components"]) == 0:
            components.remove(components[-1])
        # DM에 버튼 포함 이슈로 1차적으로 채널에 표기되도록 구현
        await direct_message(msg, http,
                             ''.join(["마지막 역전의 기회입니다.", "멀린으로 의심되는 원정대원을 선택하여 암살을 시도하세요."]),
                             discord.Colour.dark_red(), components,
                             ''.join([assassin_name, "님, 멀린을 암살하세요!"]))
    elif scope == STATUS["VIVIANE"]:
        components = [{"type": 1, "components": []}]
        # 호수의 여신 사용을 위해 가능한 원정대원에 대한 컴포넌트 설정
        viviane_name = ""
        for member in current_game.members:
            if member.viviane:
                viviane_name = member.user.name
            if member.can_viviane:
                components[-1]["components"].append({"type": 2, "label": member.user.name, "style": 3,
                                                     "custom_id": '_'.join([STATUS["VIVIANE"], member.user.name])})
            if len(components[-1]["components"]) > 0 and len(components[-1]["components"]) % 4 == 0:
                components.append({"type": 1, "components": []})
        # 마지막 ROW의 컴포넌트 값이 없는 경우 제외
        if len(components[-1]["components"]) == 0:
            components.remove(components[-1])
        # DM에 버튼 포함 이슈로 1차적으로 채널에 표기되도록 구현
        await direct_message(msg, http, "호수의 여신을 사용하여 원정대원 중 1명의 정체(선/악)를 알 수 있습니다.", discord.Colour.dark_blue(),
                             components, ''.join([viviane_name, "님, 호수의 여신을 사용하세요!"]))
