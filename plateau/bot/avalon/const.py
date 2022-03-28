# 상태
STATUS = {
    "EXIST_GAME": "EXIST_GAME",
    "RECRUIT_OK": "RECRUIT_OK",
    "NO_RECRUIT": "NO_RECRUIT",
    "ALREADY_START": "ALREADY_START",
    "MIN_MEMBER": "MIN_MEMBER",
    "MAX_MEMBER": "MAX_MEMBER",
    "NO_GAME": "NO_GAME",
    "APPLY_OK": "APPLY_OK",
    "APPLY_CANCEL": "APPLY_CANCEL",
    "START": "START",
    "END": "END",
    "GET_STATUS": "GET_STATUS",
}

# 역할자
ROLES = {
    "merlin": "멀린",
    "assassin": "암살자",
    "percival": "퍼시발",
    "mordred": "모드레드",
    "morgana": "모르가나",
    "oberon": "오베론",
    "lancelot_loyal": "랜슬롯(선)",
    "lancelot_evil": "랜슬롯(악)",
    "servant1": "선의 세력1",
    "servant2": "선의 세력2",
    "servant3": "선의 세력3",
    "servant4": "선의 세력4",
    "servant5": "선의 세력5",
    "minion1": "악의 하수인1",
    "minion2": "악의 하수인2",
    "minion3": "악의 하수인3"
}

# 플레이어 수에 따른 라운드별 원정대원 수
QUESTS = {
    5: [2, 3, 2, 3, 3],
    6: [2, 3, 4, 3, 4],
    7: [2, 3, 3, 4, 4],
    8: [3, 4, 4, 5, 5],
    9: [3, 4, 4, 5, 5],
    10: [3, 4, 4, 5, 5]
}

# 명령
COMMANDS = '''
?명령 : 가능한 모든 명령을 출력합니다.
?설명 : 게임 룰에 대한 설명을 DM으로 받습니다.
?상태 : 원정의 상태를 표시합니다.
?모집 : 원정대를 공개 모집합니다.
?참가 : 모집 중인 원정에 참가/취소합니다.
?마감 : 모집을 마감하고 원정을 준비합니다.
?시작 : 모집된 원정대로 원정을 시작합니다.
?종료 : 진행 중인 원정을 종료합니다.
'''

# 설명
EXPLAIN = '''
아발론은 마피아 장르의 보드게임입니다.
플레이어는 멀린/모드레드 팀으로 나뉘어 아서왕을 위한 원정대를 꾸리게 됩니다.
총 5번의 원정 기회가 있으며 세번의 원정을 성공/실패 시키는 팀이 승리하게 됩니다.

플레이어는 번갈아 원정대장의 역할을 수행합니다.
원정대장은 각 라운드 인원수에 맞춰 원정대를 구성하며, 모든 플레이어는 원정대에 대해 찬성/반대를 투표합니다.
찬반이 동률 혹은 반대가 과반인 경우, 다음 플레이어가 원정대장이 됩니다.
5번 연속으로 원정대 구성이 실패하는 경우는 모드레드팀이 최종승리하게 됩니다.
과반수가 찬성하는 경우, 원정을 수행하며, 원정대원들은 원정의 성공/실패를 선택합니다.
이때, 모드레드팀은 원정 실패를 시킬 수 있습니다.
'''

# 이모지 이름 prefix
EMOJI_PREFIX = 'avalon_chip_'

# 카드 이미지 prefix
CARD_PREFIX = 'avalon_card_'
