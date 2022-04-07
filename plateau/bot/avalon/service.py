import random

from game import Game
from member import Member
from const import STATUS, ROLES


def component_response(datas):
    for key, value in STATUS.items():
        if datas.get("data", {}).get("custom_id").startswith(value):
            return STATUS[key]


def status(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

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


def option(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game
    return STATUS["OPTION"]


def apply(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

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
        # 참가자 인원에 맞춰서 games의 역할자 추가
        current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
        return STATUS["APPLY"]
    else:
        # 플레이어가 이미 참가상태인 경우, 해당 원정에서 제외
        current_game.remove_member(user)
        # 참가자 인원에 맞춰서 games의 역할자 추가
        current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
        return STATUS["APPLY_CANCEL"]


def percival_morgana(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 퍼시발/모르가나 옵션을 on=off
    current_game.percival = not current_game.percival
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def mordred(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 모드레드 옵션을 on=off
    current_game.mordred = not current_game.mordred
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def oberon(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 오베론 옵션을 on=off
    current_game.oberon = not current_game.oberon
    # 참가자 인원에 맞춰서 games의 역할자 추가
    current_game.roles = 5 if len(current_game.members) < 5 else len(current_game.members)
    return STATUS["STATUS"]


def anonymous(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]

    # 해당 게임의 익명 옵션을 on=off
    current_game.anonymous = not current_game.anonymous
    return STATUS["STATUS"]


def commence(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS["ALREADY_START"]
    # 총 참가인원(5명 이상 ~ 10명 이하) 점검
    elif len(current_game.members) < 5:
        return STATUS["MIN_MEMBER"]
    elif len(current_game.members) > 10:
        return STATUS["MAX_MEMBER"]

    # 시작 전, Lock 처리
    for member in current_game.members:
        if user.name == member.user.name:
            current_game.lock_member = member

    # 원정 시작 전 기본 데이터 초기화
    current_game.clear_game()
    # 원정 시작 상태 값 변경
    current_game.expedition = True
    # 멤버들 원정 순서 랜덤 처리 및 직업 배정
    roles = current_game.roles["loyal"] + current_game.roles["evil"]
    random.shuffle(current_game.members)
    random.shuffle(roles)
    for member in current_game.members:
        member.role = roles.pop()
        member.viviane = False
        member.can_viviane = True
    current_game.quest_round = 1
    current_game.leader = current_game.members[0]
    current_game.members[-1].viviane = True
    current_game.members[-1].can_viviane = False
    # 호수의 여인(비비안) 사용을 위해 게임의 비비안 사용 가능 멤버 추가
    current_game.viviane.append(current_game.members[-1])
    return STATUS["COMMENCE"]


def initial(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정의 정보를 초기화(역할, 시작여부, 라운드, 부결회수)
    current_game.clear_game()
    return STATUS["INITIAL"]


def organize(msg, games, datas, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정대장이 아닌 경우, 권한없음 메시지 출력
    if user != current_game.leader.user:
        return STATUS["NO_PERMISSION"]

    # 원정대장인 경우, 현재까지 설정된 원정대원이 해당 라운드의 대원수보다 적은 경우에 원정대원에 추가
    username = datas.get("data", {}).get("custom_id").split('_')[-1]
    for member in current_game.members:
        if username == member.user.name:
            # 기존에 등록한 원정대원이면 제거
            if member in current_game.rounds[current_game.quest_round]["members"]:
                current_game.rounds[current_game.quest_round]["members"].remove(member)
                return STATUS["ORGANIZE"]
            # 등록되지 않은 원정대원이면 추가
            else:
                if current_game.rounds[current_game.quest_round]["players"] > len(
                        current_game.rounds[current_game.quest_round]["members"]):
                    current_game.rounds[current_game.quest_round]["members"].append(member)
                    return STATUS["ORGANIZE"]
                else:
                    return STATUS["MAX_ORGANIZE"]
    return STATUS["NO_MEMBER"]


def proposal(msg, games, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정대장이 아닌 경우, 권한없음 메시지 출력
    if user != current_game.leader.user:
        return STATUS["NO_PERMISSION"]

    # 원정대장인 경우, 현재까지 설정된 원정대원의 수가 해당 라운드의 대원수와 같은 경우 제안
    if current_game.rounds[current_game.quest_round]["players"] == len(
            current_game.rounds[current_game.quest_round]["members"]):
        return STATUS["PROPOSAL"]
    else:
        return STATUS["MIN_ORGANIZE"]


def vote(msg, games, user, result):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정멤버가 아닌 경우, 권한없음 메시지 출력
    is_member = False
    for member in current_game.members:
        if user == member.user:
            is_member = True
            # 원정결과 전, Lock 처리
            current_game.lock_member = member
            break
    if not is_member:
        return STATUS["NO_PERMISSION"]

    # 게임 라운드의 투표내역에 입력(result True이면 approval, True이면 reject)
    for member in current_game.members:
        if user == member.user:
            # 투표 결과 저장 전, 기 저장된 투표 결과 삭제
            if member in current_game.rounds[current_game.quest_round]["vote"]["approval"]:
                current_game.rounds[current_game.quest_round]["vote"]["approval"].remove(member)
            if member in current_game.rounds[current_game.quest_round]["vote"]["reject"]:
                current_game.rounds[current_game.quest_round]["vote"]["reject"].remove(member)

            # 투표 결과가 찬성인 경우,
            if result:
                current_game.rounds[current_game.quest_round]["vote"]["approval"].append(member)
                return STATUS["APPROVE"]
            # 투표 결과가 반대인 경우,
            else:
                current_game.rounds[current_game.quest_round]["vote"]["reject"].append(member)
                return STATUS["REJECT"]

    return STATUS["NO_MEMBER"]


def quest(msg, games, user, result):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 원정멤버가 아닌 경우, 권한없음 메시지 출력
    is_member = False
    for member in current_game.rounds[current_game.quest_round]["members"]:
        if user == member.user:
            is_member = True
            # 원정결과 전, Lock 처리
            current_game.lock_member = member
            break
    if not is_member:
        return STATUS["NO_PERMISSION"]

    # 게임 라운드의 결과내역에 입력(result True이면 success, True이면 fail)
    for member in current_game.members:
        if user == member.user:
            if not result and member.role in current_game.roles["loyal"]:
                return STATUS["LOYAL_FAIL"]
            # 이미 제출했으나, 상호작용 실패로 최종 결과가 되지 않은 경우 처리를 위해
            total_member = current_game.rounds[current_game.quest_round]["members"]
            success_member = current_game.rounds[current_game.quest_round]["result"]["success"]
            fail_member = current_game.rounds[current_game.quest_round]["result"]["fail"]
            # 기 제출된 성공/실패 건수가 해당 라운드의 원정대원 수와 같으면 결과 처리
            if len(total_member) == len(success_member) + len(fail_member):
                if result:
                    return STATUS["QUEST_SUCCESS"]
                else:
                    return STATUS["QUEST_FAIL"]
            else:
                if member in current_game.rounds[current_game.quest_round]["result"]["success"]:
                    return STATUS["ALREADY_RESULT"]
                elif member in current_game.rounds[current_game.quest_round]["result"]["fail"]:
                    return STATUS["ALREADY_RESULT"]
                if result:
                    current_game.rounds[current_game.quest_round]["result"]["success"].append(member)
                    return STATUS["QUEST_SUCCESS"]
                else:
                    current_game.rounds[current_game.quest_round]["result"]["fail"].append(member)
                    return STATUS["QUEST_FAIL"]

    return STATUS["NO_MEMBER"]


def assassin(msg, games, datas, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 암살자가 아닌 경우, 권한없음 메시지 출력
    for member in current_game.members:
        if user == member.user:
            if member.role != ROLES["assassin"]:
                return STATUS["NO_PERMISSION"]

    # 암살자인 경우, 암살 대상이 멀린인 경우 암살 성공, 그 외는 암살 실패
    username = datas.get("data", {}).get("custom_id").split('_')[-1]
    # 원정 시작 상태 값 변경
    current_game.expedition = False
    for member in current_game.members:
        if username == member.user.name:
            if member.role == ROLES["merlin"]:
                return STATUS["ASSASSIN"]
    return STATUS["ASSASSIN_FAIL"]


def viviane(msg, games, datas, user):
    current_game = check_game(msg, games, user)
    if current_game in (STATUS["NO_RECRUIT"], STATUS["NO_GAME"], STATUS["LOCK_GAME"]):
        return current_game

    # 호수의 여신이 없는 경우, 권한없음 메시지 출력
    for member in current_game.members:
        if user == member.user:
            if not member.viviane:
                return STATUS["NO_PERMISSION"]

    # 호수의 여신으로 선택한 멤버의 선/악에 따라 응답
    username = datas.get("data", {}).get("custom_id").split('_')[-1]
    for member in current_game.members:
        if user == member.user:
            # 현재 호수의 여신 원정대원의 상태 변경
            member.viviane = False
        if username == member.user.name:
            # 정체 확인 원정대원의 상태 변경
            member.viviane = True
            member.can_viviane = False
            current_game.viviane.append(member)
            if member.role in (current_game.roles["loyal"]):
                return STATUS["VIVIANE_LOYAL"]
            else:
                return STATUS["VIVIANE_EVIL"]
    return STATUS["NO_MEMBER"]


def check_game(msg, games, user):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS["NO_RECRUIT"]
    current_game = games[msg.channel.id]["game"]
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS["NO_GAME"]
    # 게임의 Lock 여부 점검
    if current_game.lock_member:
        if user.name != current_game.lock_member.user.name:
            return STATUS["LOCK_GAME"]
    return current_game


def check_vote(current_game):
    # 멤버 전체가 투표한 경우,
    total_member = len(current_game.members)
    approval_member = len(current_game.rounds[current_game.quest_round]["vote"]["approval"])
    reject_member = len(current_game.rounds[current_game.quest_round]["vote"]["reject"])
    if total_member == approval_member + reject_member:
        # 찬성/반대 수에 따라서 라운드 clear 혹은 다음 라운드 진행
        # 찬성이 과반이 경우에만 원정 진행
        if approval_member > reject_member:
            return STATUS["EXPEDITION_ROUND"]
        else:
            # deny 건수 + 1
            current_game.rounds[current_game.quest_round]["deny"] = \
                current_game.rounds[current_game.quest_round]["deny"] + 1
            # 라운드의 원정멤버 구성 초기화
            current_game.rounds[current_game.quest_round]["members"] = []
            chk_endgame = check_endgame(current_game)
            if chk_endgame == STATUS["TERMINATE_LOYAL"]:
                return STATUS["TERMINATE_LOYAL"]
            elif chk_endgame == STATUS["TERMINATE_EVIL"]:
                return STATUS["TERMINATE_EVIL"]
            else:
                return STATUS["ORGANIZE_ROUND"]


def next_vote(current_game):
    total_member = len(current_game.members)

    # 라운드의 투표 결과 초기화
    current_game.rounds[current_game.quest_round]["vote"] = {"approval": [], "reject": []}
    # 원정대장 변경
    current_game.leader = \
        current_game.members[(current_game.members.index(current_game.leader) + 1) % total_member]


def check_quest(current_game):
    # 라운드의 원정 멤버 전체가 투표한 경우,
    total_member = len(current_game.rounds[current_game.quest_round]["members"])
    success_member = len(current_game.rounds[current_game.quest_round]["result"]["success"])
    fail_member = len(current_game.rounds[current_game.quest_round]["result"]["fail"])
    if total_member == success_member + fail_member:
        # 원정대장 변경
        current_game.leader = \
            current_game.members[(current_game.members.index(current_game.leader) + 1) % len(current_game.members)]
        # 해당 라운드 종료 처리
        current_game.rounds[current_game.quest_round]["terminate"] = True
        # 투표결과 게임이 종료 여부에 대한 점검
        chk_endgame = check_endgame(current_game)
        if chk_endgame == STATUS["TERMINATE_LOYAL"]:
            return STATUS["TERMINATE_LOYAL"]
        elif chk_endgame == STATUS["TERMINATE_EVIL"]:
            return STATUS["TERMINATE_EVIL"]
        else:
            # 게임이 종료되지 않으면 다음 라운드로 진행
            current_game.quest_round += 1
            # 호수의 여신(비비안)이 있고(모드레드/오베론 있는 경우), 2라운드 이상인 경우, 호수의 여신 처리(5라운드 제외)
            if 2 < current_game.quest_round <= 5 and (current_game.mordred or current_game.oberon):
                return STATUS["VIVIANE"]
            return STATUS["ORGANIZE_QUEST"]


def check_endgame(current_game):
    # 게임 원정 부결건수가 5회 이상인 라운드 점검
    if current_game.rounds[current_game.quest_round]["deny"] >= 5:
        return STATUS["TERMINATE_EVIL"]

    # 게임 라운드의 원정 결과가 3회 이상 성공/실패가 있는지 점검
    if current_game.quest_round >= 3:
        success_round = 0
        fail_round = 0
        for _round in range(current_game.quest_round):
            # 7명 이상 게임의 4라운드인 경우는 2명 이상 실패여야 실패
            if current_game.fourth_round and _round + 1 == 4:
                if len(current_game.rounds[_round + 1]["result"]["fail"]) >= 2:
                    fail_round += 1
                elif len(current_game.rounds[_round + 1]["result"]["success"]) > 0:
                    success_round += 1
            else:
                if len(current_game.rounds[_round + 1]["result"]["fail"]) > 0:
                    fail_round += 1
                elif len(current_game.rounds[_round + 1]["result"]["success"]) > 0:
                    success_round += 1
        if fail_round >= 3:
            # 원정 시작 상태 값 변경
            current_game.expedition = False
            return STATUS["TERMINATE_EVIL"]
        if success_round >= 3:
            return STATUS["TERMINATE_LOYAL"]

    return ""
