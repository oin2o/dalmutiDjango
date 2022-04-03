import random

from game import Game
from member import Member
from const import STATUS


def component_response(datas):
    if datas.get("type") == 3:
        for key, value in STATUS.items():
            if datas.get("data", {}).get("custom_id") == value:
                return STATUS[key]


def status(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    return STATUS["STATUS"]


def recruit(msg, games, user):
    if msg.channel.id not in games:
        # 원정 처리를 위한 게임 데이터 저장소 생성
        current_game = {"game": Game(msg.channel)}
        # 게임 멤버에 현재 사용자 추가
        current_game["game"].add_member(Member(user))
        # 전체 게임 객체에 현재 게임 추가
        games[msg.channel.id] = current_game
    return STATUS["RECRUIT"]


def dismission(msg, games):
    if msg.channel.id in games:
        # 해당 채널 게임 데이터 삭제
        games.pop(msg.channel.id)
    return STATUS["DISMISSION"]


def apply(msg, games, user):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]
    # 총 참가인원(10명 이하) 점검
    elif len(current_game.members) >= 10:
        return STATUS["MAX_MEMBER"]

    # 플레이어가 기참가 여부 조회
    already_apply = False
    for member in current_game.members:
        if member.user == user:
            already_apply = True
    if not already_apply:
        # 플레이어가 미참가인 경우, 해당 원정에 참가시킴
        current_game.add_member(Member(user))
        return STATUS["APPLY"]
    else:
        # 플레이어가 이미 참가상태인 경우, 해당 원정에서 제외
        current_game.remove_member(user)
        return STATUS["APPLY_CANCEL"]

    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["APPLY"]


def psercival_morgana(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 퍼시발/모르가나 옵션을 on=off
    current_game.percival = not current_game.percival
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def modred(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 모드레드 옵션을 on=off
    current_game.mordred = not current_game.mordred
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def oberon(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 오베론 옵션을 on=off
    current_game.oberon = not current_game.oberon
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def anonymous(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 익명 옵션을 on=off
    current_game.anonymous = not current_game.anonymous
    return STATUS["STATUS"]


def commence(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]
    # 총 참가인원(5명 이상 ~ 10명 이하) 점검
    elif len(current_game.members) < 5:
        return STATUS["MIN_MEMBER"]
    elif len(current_game.members) > 10:
        return STATUS["MAX_MEMBER"]

    # 원정 시작 상태 값 변경
    current_game.expedition = True
    # 멤버들 원정 순서 랜덤 처리 및 직업 배정
    roles = current_game.roles["loyal"] + current_game.roles["evil"]
    random.shuffle(current_game.members)
    random.shuffle(roles)
    for member in current_game.members:
        member.role = roles.pop()
    current_game.leader = current_game.members[0]
    current_game.members[-1].viviane = True
    # 호수의 여인(비비안) 사용을 위해 게임의 비비안 사용 가능 멤버 추가
    current_game.viviane = current_game.members[:-1]

    # 개인메시지로 역할 및 직업 정보 보내기

    return STATUS["COMMENCE"]


def initial(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]

    # 원정의 정보를 초기화(역할, 시작여부, 라운드, 부결회수)
    current_game.clear_game()
    return STATUS["INITIAL"]
