from const import ROLES, EMOJI_PREFIX


def get_emoji(msg, role_kr, roles, emojis):
    # 이모지 표기 문자열 추가(디스코드 서버에 파일명과 동일하게 추가 필요)
    return ''.join(["<:", roles[role_kr["name"]], ":", str(emojis[msg.guild.id][''.join([EMOJI_PREFIX, roles[role_kr["name"]]])]), ">"])


def get_explain(msg, roles, emojis):
    return '\n'.join([
        "‣ 멀린팀",
        ' '.join([get_emoji(msg, ROLES["merlin"], roles, emojis), "멀린 : 모드레드를 제외한 악을 알고 있습니다."]),
        ' '.join([get_emoji(msg, ROLES["percival"], roles, emojis), "퍼시발 : 멀린/모르가나가 보이지만, 정체는 모릅니다."]),
        ' '.join(
            [get_emoji(msg, ROLES["servant1"], roles, emojis), get_emoji(msg, ROLES["servant2"], roles, emojis),
             get_emoji(msg, ROLES["servant3"], roles, emojis), get_emoji(msg, ROLES["servant4"], roles, emojis),
             get_emoji(msg, ROLES["servant5"], roles, emojis), "선의 세력 : 원정을 성공 시키십시오."]),
        "",
        "‣ 모드레드팀",
        ' '.join([get_emoji(msg, ROLES["mordred"], roles, emojis), "모드레드 : 멀린에게 정체가 보이지 않습니다."]),
        ' '.join([get_emoji(msg, ROLES["morgana"], roles, emojis), "모르가나 : 퍼시발에게 멀린으로 위장합니다."]),
        ' '.join([get_emoji(msg, ROLES["assassin"], roles, emojis), "암살자 : 멀린을 암살할 수 있습니다."]),
        ' '.join([get_emoji(msg, ROLES["oberon"], roles, emojis), "오베론 : 악의 하수인과 서로 정체를 모릅니다."]),
        ' '.join(
            [get_emoji(msg, ROLES["minion1"], roles, emojis), get_emoji(msg, ROLES["minion2"], roles, emojis),
             get_emoji(msg, ROLES["minion3"], roles, emojis), "악의 하수인 : 원정을 실패 시키십시오."]),
        "",
        "‣ 제3세력",
        "▪️ 랜슬롯 : 선/악 모두 존재하며, 원정 중, 팀을 배신할 수 있습니다."
    ])


def get_status(msg, current_game, roles, emojis):
    name = []
    desc = [': '.join(["‣ 원정상태", "원정중" if current_game.expedition else "모집중"])]
    for member in current_game.members:
        name.append(member.user_name)
    desc.append("‣ 원정구성")
    desc.append('• '.join(["\t", ', '.join(name)]))
    loyal_emoji = []
    evil_emoji = []
    for role_kr in current_game.roles['loyal']:
        loyal_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    for role_kr in current_game.roles['evil']:
        evil_emoji.append(get_emoji(msg, role_kr, roles, emojis))
    desc.append(': '.join(["\t• 멀린팀", ' '.join(loyal_emoji)]))
    desc.append(': '.join(["\t• 모드레드팀", ' '.join(evil_emoji)]))

    return '\n'.join(desc)
