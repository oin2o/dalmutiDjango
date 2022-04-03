from const import ROLES, ROLES_REVERSE, CHIPS, EMOJI_PREFIX
from data import emojis


def get_emoji(msg, role_kr, scope="roles"):
    # 이모지 표기 문자열 추가(디스코드 서버에 파일명과 동일하게 추가 필요)
    if scope == "roles":
        return ''.join(["<:", ROLES_REVERSE[role_kr["name"]], ":", str(emojis[msg.guild.id][''.join(
            [EMOJI_PREFIX, ROLES_REVERSE[role_kr["name"]]])]), ">"])
    else:
        return ''.join(["<:", CHIPS[role_kr], ":", str(emojis[msg.guild.id][CHIPS[role_kr]]), ">"])


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
        "▪️ 랜슬롯 : 선/악 모두 존재하며, 원정 중, 팀을 배신할 수 있습니다."
    ])


def get_status(msg, current_game):
    name = []
    desc = [": ".join(["‣ 원정상태", "원정중" if current_game.expedition else "모집중"])]
    for member in current_game.members:
        name.append(member.user.name)
    desc.append(": ".join(["‣ 원정투표", "익명" if current_game.anonymous else "공개"]))
    desc.append(''.join(["‣ 원정구성", "(4라운드 실패 2장 필요)" if current_game.fourth_round else ""]))
    desc.append("  ".join(["••• ", ", ".join(name)]))
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
        rounds.append(get_emoji(msg, ''.join([EMOJI_PREFIX, '_'.join([str(5 if len(
            current_game.members) < 5 else 8 if len(current_game.members) > 8 else len(current_game.members)),
                                                                      str(_round)])]), "chips"))
    desc.append(": ".join(["••• 라운드", ' '.join(rounds)]))
    return '\n'.join(desc)
