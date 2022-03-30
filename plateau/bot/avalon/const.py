# 상태
STATUS = {
    "COMMANDS": "명령",
    "AVALON": "아발론",
    "EXPLAIN": "설명",
    "STATUS": "상태",
    "RECRUIT": "모집",
    "RECRUIT_DISABLE": "모집_비활성",
    "DISMISSION": "해산",



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
    "APPLY_BUTTON": "APPLY_BUTTON",
    "START_BUTTON": "START_BUTTON",
    "END_BUTTON": "END_BUTTON",
    "STATUS_BUTTON": "STATUS_BUTTON",
}

# 버튼
BUTTONS = {
    STATUS["AVALON"]: {"type": 2, "label": STATUS["AVALON"], "style": 1, "custom_id": STATUS["AVALON"], "disabled": False},
    STATUS["EXPLAIN"]: {"type": 2, "label": STATUS["EXPLAIN"], "style": 2, "custom_id": STATUS["EXPLAIN"], "disabled": False},
    STATUS["STATUS"]: {"type": 2, "label": STATUS["STATUS"], "style": 3, "custom_id": STATUS["STATUS"], "disabled": False},
    STATUS["RECRUIT"]: {"type": 2, "label": STATUS["RECRUIT"], "style": 1, "custom_id": STATUS["RECRUIT"], "disabled": False},
    STATUS["RECRUIT_DISABLE"]: {"type": 2, "label": STATUS["RECRUIT"], "style": 1, "custom_id": STATUS["RECRUIT_DISABLE"], "disabled": True},
    STATUS["DISMISSION"]: {"type": 2, "label": STATUS["DISMISSION"], "style": 4, "custom_id": STATUS["DISMISSION"], "disabled": False},
}

# 역할자
INTERACTION_SCOPE = {
    "공개": 0,
    "개인": 64,
}

# 역할자
ROLES = {
    "merlin": {"name": "멀린", "order": 1},
    "percival": {"name": "퍼시발", "order": 2},
    "assassin": {"name": "암살자", "order": 1},
    "morgana": {"name": "모르가나", "order": 2},
    "mordred": {"name": "모드레드", "order": 4},
    "oberon": {"name": "오베론", "order": 5},
    "lancelot_loyal": {"name": "랜슬롯(선)", "order": 3},
    "lancelot_evil": {"name": "랜슬롯(악)", "order": 3},
    "servant1": {"name": "선의 세력1", "order": 4},
    "servant2": {"name": "선의 세력2", "order": 5},
    "servant3": {"name": "선의 세력3", "order": 6},
    "servant4": {"name": "선의 세력4", "order": 7},
    "servant5": {"name": "선의 세력5", "order": 8},
    "minion1": {"name": "악의 하수인1", "order": 6},
    "minion2": {"name": "악의 하수인2", "order": 7},
    "minion3": {"name": "악의 하수인3", "order": 8},
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
=명령 : 가능한 모든 명령을 출력합니다.
=설정 : 필요한 이모지를 디스코드 서버에 등록(1회)합니다.
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
