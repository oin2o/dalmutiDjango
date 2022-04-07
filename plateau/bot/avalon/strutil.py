from const import ROLES, ROLES_REVERSE, CHIPS, EMOJI_PREFIX
from data import emojis


def get_emoji(msg, role_name, scope="roles"):
    # 이모지 표기 문자열 추가(디스코드 서버에 파일명과 동일하게 추가 필요)
    if scope == "roles":
        return ''.join(["<:", ROLES_REVERSE[role_name["name"]], ":", str(emojis[msg.guild.id][''.join(
            [EMOJI_PREFIX, ROLES_REVERSE[role_name["name"]]])]), ">"])
    else:
        return ''.join(["<:", CHIPS[role_name], ":", str(emojis[msg.guild.id][CHIPS[role_name]]), ">"])


def get_explain(msg):
    return '\n'.join([
        "‣ 멀린팀",
        ' '.join([get_emoji(msg, ROLES["merlin"]), "멀린 : 모드레드를 제외한 악을 알고 있습니다."]),
        ' '.join([get_emoji(msg, ROLES["percival"]), "퍼시발 : 멀린/모르가나가 보이지만, 정체는 모릅니다."]),
        ' '.join(
            [get_emoji(msg, ROLES["guinevere"]), get_emoji(msg, ROLES["servant1"]),
             get_emoji(msg, ROLES["servant2"]), get_emoji(msg, ROLES["servant3"]),
             get_emoji(msg, ROLES["servant4"]), "선의 세력 : 원정을 성공 시키십시오."]),
        "",
        "‣ 모드레드팀",
        ' '.join([get_emoji(msg, ROLES["mordred"]), "모드레드 : 멀린에게 정체가 보이지 않습니다."]),
        ' '.join([get_emoji(msg, ROLES["morgana"]), "모르가나 : 퍼시발에게 멀린으로 위장합니다."]),
        ' '.join([get_emoji(msg, ROLES["assassin"]), "암살자 : 멀린을 암살할 수 있습니다."]),
        ' '.join([get_emoji(msg, ROLES["oberon"]), "오베론 : 악의 하수인과 서로 정체를 모릅니다."]),
        ' '.join(
            [get_emoji(msg, ROLES["minion1"]), get_emoji(msg, ROLES["minion2"]),
             get_emoji(msg, ROLES["minion3"]), "악의 하수인 : 원정을 실패 시키십시오."]),
        "",
        "‣ 제3세력",
        "▪️ 랜슬롯 : 선/악 모두 존재하며, 원정 중, 팀을 배신할 수 있습니다.",
        "▪️ 비비안 : 원정대원의 선/악을 알려줍니다.",
    ])


def get_status(msg, current_game):
    name = []
    desc = [": ".join(["‣ 원정상태", "원정중" if current_game.expedition else "모집중"])]
    for member in current_game.members:
        name.append(member.user.name)
    desc.append("\n‣ 원정설정")
    desc.append(": ".join(["••• 투표결과", "익명" if current_game.anonymous else "공개"]))
    if current_game.percival or current_game.mordred or current_game.oberon or current_game.lancelot:
        desc.append(": ".join(["••• 특수", " ".join(["퍼시발/모르가나" if current_game.percival else "",
                                                   "모드레드" if current_game.mordred else "",
                                                   "오베론" if current_game.oberon else "",
                                                   "랜슬롯" if current_game.lancelot else ""])]))
    if current_game.mordred or current_game.oberon:
        desc.append("••• 호수의 여신(비비안) 포함")
    desc.append(''.join(["\n‣ 원정구성", "(4라운드 실패 2장 필요)" if current_game.fourth_round else ""]))
    desc.append(''.join(["••• ", ", ".join(name)]))
    loyal_emoji = []
    evil_emoji = []
    for role_kr in current_game.roles["loyal"]:
        loyal_emoji.append(get_emoji(msg, role_kr))
    for role_kr in current_game.roles["evil"]:
        evil_emoji.append(get_emoji(msg, role_kr))
    desc.append(": ".join(["••• 멀린팀", ' '.join(loyal_emoji)]))
    desc.append(": ".join(["••• 모드레드팀", ' '.join(evil_emoji)]))
    rounds = []
    for _round in current_game.rounds:
        # 해당 라운드가 종료된 경우, 결과 이모지를 추가하고, 그 외에는 라운드별 인원수를 표기
        if current_game.rounds[_round]["terminate"]:
            if len(current_game.rounds[_round]["result"]["fail"]) > 0:
                rounds.append(get_emoji(msg, ''.join([EMOJI_PREFIX, "fail"]), "chips"))
            else:
                rounds.append(get_emoji(msg, ''.join([EMOJI_PREFIX, "success"]), "chips"))
        else:
            rounds.append(get_emoji(msg,
                                    ''.join([EMOJI_PREFIX,
                                             '_'.join([str(5 if len(current_game.members) < 5 else
                                                           8 if len(current_game.members) > 8 else
                                                           len(current_game.members)),
                                                       str(_round)])]), "chips"))
    desc.append(": ".join(["••• 라운드", ' '.join(rounds)]))
    deny_emoji = []
    if current_game.quest_round > 0:
        for _ in range(current_game.rounds[current_game.quest_round]["deny"]):
            deny_emoji.append(get_emoji(msg, CHIPS[''.join([EMOJI_PREFIX, "deny"])], "chips"))
        if len(deny_emoji) > 0:
            desc.append(": ".join(["••• 부결", ' '.join(deny_emoji)]))
        if current_game.quest_round > 1:
            if current_game.quest_round > 2 and (current_game.mordred or current_game.oberon):
                desc.append("\n‣ 호수의 여신")
                viviane_desc = []
                for member in current_game.viviane:
                    viviane_desc.append(member.user.name)
                desc.append(''.join(["••• ", " > ".join(viviane_desc)]))
            desc.append("\n‣ 원정결과")
            for i in range(1, 6):
                if current_game.rounds[i]["terminate"]:
                    success_count = len(current_game.rounds[i]["result"]["success"])
                    fail_count = len(current_game.rounds[i]["result"]["fail"])
                    round_desc = []
                    for j in range(success_count + fail_count):
                        if j < fail_count:
                            round_desc.append(get_emoji(msg, CHIPS[''.join([EMOJI_PREFIX, "quest_fail"])], "chips"))
                        else:
                            round_desc.append(get_emoji(msg, CHIPS[''.join([EMOJI_PREFIX, "quest_success"])], "chips"))
                    for member in current_game.rounds[i]["members"]:
                        round_desc.append(''.join([" ", member.user.name]))
                    desc.append(''.join([''.join(["••• ", str(i), "라운드: "]), ''.join(round_desc)]))
                else:
                    break
    if not current_game.expedition and current_game.quest_round > 0:
        desc.append("\n‣ 원정대 역할")
        member_roles = []
        for member in current_game.members:
            member_roles.append(": ".join([''.join(["••• ", member.user.name]), get_emoji(msg, member.role)]))
        desc.append('\n'.join(member_roles))
    return '\n'.join(desc)


def get_role(current_game, member):
    desc = []
    if member.role == ROLES["merlin"]:
        desc.append("모드레드를 제외한 악의 하수인들을 알고 있지만, 암살자를 조심하세요.")
        desc.append("‣ 모드레드를 제외한 악의 하수인" if current_game.mordred else "‣ 악의 하수인")
        for evils in current_game.members:
            if "evil" == evils.role["lawful"] and evils.role["name"] not in "모드레드":
                desc.append(''.join(["••• ", evils.user.name]))
    elif member.role == ROLES["percival"]:
        desc.append("악의 하수인에게 속지 말고, 멀린을 찾아 원정을 성공 시키십시오.")
        desc.append("‣ 멀린 혹은 모르가나")
        for merlins in current_game.members:
            if merlins.role in (ROLES["merlin"], ROLES["morgana"]):
                desc.append(''.join(["••• ", merlins.user.name]))
    elif member.role == ROLES["assassin"]:
        desc.append("선의 세력을 속여 원정을 실패 시키십시오. 원정이 성공하는 경우, 멀린을 암살하여 악의 세력을 승리 시키십시오.")
        desc.append("‣ 오베론을 제외한 악의 하수인" if current_game.oberon else "‣ 악의 하수인")
        for evils in current_game.members:
            if "evil" == evils.role["lawful"] and evils.role["name"] not in "오베론":
                desc.append(''.join(["••• ", evils.user.name]))
    elif member.role == ROLES["morgana"]:
        desc.append("퍼시발에게 멀린으로 위장하였습니다. 퍼시발을 현혹시키고 원정을 실패 시키십시오.")
        desc.append("‣ 오베론을 제외한 악의 하수인" if current_game.oberon else "‣ 악의 하수인")
        for evils in current_game.members:
            if "evil" == evils.role["lawful"] and evils.role["name"] not in "오베론":
                desc.append(''.join(["••• ", evils.user.name]))
    elif member.role == ROLES["mordred"]:
        desc.append("멀린에게 정체를 들키지 않았습니다. 선의 세력 사이에 숨어 원정을 실패 시키십시오.")
        desc.append("‣ 오베론을 제외한 악의 하수인" if current_game.oberon else "‣ 악의 하수인")
        for evils in current_game.members:
            if "evil" == evils.role["lawful"] and evils.role["name"] not in "오베론":
                desc.append(''.join(["••• ", evils.user.name]))
    elif member.role == ROLES["oberon"]:
        desc.append("다른 악을 알 수 없습니다. 악의 하수인을 찾고, 선의 세력을 속여 원정을 실패 시키십시오.")
    elif member.role in (ROLES["lancelot_loyal"], ROLES["lancelot_evil"]):
        desc.append("선/악 모두 될 수 있습니다. 배신의 기회를 노리세요.")
        if member.role == ROLES["lancelot_evil"]:
            desc.append("‣ 오베론을 제외한 악의 하수인" if current_game.oberon else "‣ 악의 하수인")
            for evils in current_game.members:
                if "evil" == evils.role["lawful"] and evils.role["name"] not in "오베론":
                    desc.append(''.join(["••• ", evils.user.name]))
    elif member.role in (ROLES["guinevere"], ROLES["servant1"], ROLES["servant2"], ROLES["servant3"],
                         ROLES["servant4"]):
        desc.append("악의 하수인에게 속지 말고 원정을 성공 시키십시오.")
    elif member.role in (ROLES["minion1"], ROLES["minion2"], ROLES["minion3"]):
        desc.append("선의 세력을 속여 원정을 실패 시키십시오.")
        desc.append("‣ 오베론을 제외한 악의 하수인" if current_game.oberon else "‣ 악의 하수인")
        for evils in current_game.members:
            if "evil" == evils.role["lawful"] and evils.role["name"] not in "오베론":
                desc.append(''.join(["••• ", evils.user.name]))
    return '\n'.join(desc)
