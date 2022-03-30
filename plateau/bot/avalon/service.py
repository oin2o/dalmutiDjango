from game import Game
from member import Member
from const import STATUS


def recruit(msg, games):
    # 채널에 미리 시작된 원정이 있는 경우는 추가 모집하지 않음
    if msg.channel.id in games:
        return STATUS['EXIST_GAME']
    # 원정 처리를 위한 게임 데이터 저장소 생성
    current_game = {'game': Game(msg.channel)}
    # 게임 멤버에 현재 사용자 추가
    current_game['game'].add_member(Member(msg.author))
    # 전체 게임 객체에 현재 게임 추가
    games[msg.channel.id] = current_game
    return STATUS['RECRUIT_OK']


def apply(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS['NO_RECRUIT']
    current_game = games[msg.channel.id]['game']
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS['NO_GAME']
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS['ALREADY_START']
    # 총 참가인원(10명 이하) 점검
    elif len(current_game.members) >= 10:
        return STATUS['MAX_MEMBER']
    '''
    # 플레이어가 미참가인 경우, 해당 원정에 참가시킴
    if msg.message.author not in current_game.members:
        current_game.add_member(Member(msg.message.author))
        return STATUS['APPLY_OK']
    # 플레이어가 이미 참가상태인 경우, 해당 원정에서 제외
    else:
        current_game.remove_member(Member(msg.message.author))
        return STATUS['APPLY_CANCEL']
    '''
    current_game.add_member(Member(msg.message.author))
    return STATUS['APPLY_OK']


def expedition(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS['NO_RECRUIT']
    current_game = games[msg.channel.id]['game']
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS['NO_GAME']
    # 원정 시작여부 점검(미시작 중에는 모집)
    elif current_game.expedition:
        return STATUS['ALREADY_START']
    # 총 참가인원(5명 이상 ~ 10명 이하) 점검
    elif len(current_game.members) < 5:
        return STATUS['MIN_MEMBER']
    elif len(current_game.members) > 10:
        return STATUS['MAX_MEMBER']
    # 원정 시작 상태 값 변경
    current_game.expedition = True
    # 멤버들 원정순서 랜덤 처리
    # 멤버수에 맞춰서 역할 객체 조정
    # 멤버별 직업 랜덤 처리
    return STATUS['START']


def end(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS['NO_RECRUIT']
    current_game = games[msg.channel.id]['game']
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS['NO_GAME']
    # 원정의 정보를 초기화(역할, 시작여부, 라운드, 부결회수)
    current_game.clear_game()
    return STATUS['END']


def status(msg, games):
    # 채널에 시작된 원정이 있는지 점검
    if msg.channel.id not in games:
        return STATUS['NO_RECRUIT']
    current_game = games[msg.channel.id]['game']
    # 게임의 객체 정상여부 점검
    if not current_game:
        return STATUS['NO_GAME']
    return STATUS['GET_STATUS']


def component_response(datas):
    if datas.get("type") == 3:
        for key, value in STATUS.items():
            if datas.get("data", {}).get("custom_id") == value:
                return STATUS[key]
