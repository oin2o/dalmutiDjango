# 상태
STATUS = {
    "COMMANDS": "명령",
    "AVALON": "아발론",
    "EXPLAIN": "설명",
    "STATUS": "상태",
    "RECRUIT": "모집",
    "DISMISSION": "해산",
    "APPLY": "참가",
    "OPTION": "옵션",
    "COMMENCE": "시작",
    "INITIAL": "초기화",
    "PERCIVAL_MORGANA": "퍼/모",
    "MORDRED": "모드레드",
    "OBERON": "오베론",
    "ANONYMOUS": "익명",
    "NO_RECRUIT": "원정_미존재",
    "NO_GAME": "아발론_미존재",
    "ALREADY_START": "이미_시작됨",
    "MAX_MEMBER": "멤버초과",
    "MIN_MEMBER": "멤버미만",
    "APPLY_CANCEL": "참가취소",
    "ORGANIZE": "원정구성",
    "PROPOSAL": "원정제안",
    "NO_PERMISSION": "권한없음",
    "MAX_ORGANIZE": "원정대초과",
    "MIN_ORGANIZE": "원정대미만",
    "APPROVE": "찬성",
    "REJECT": "반대",
    "NO_MEMBER": "멤버아님",
    "EXPEDITION_ROUND": "원정라운드",
    "ORGANIZE_ROUND": "원정재구성",
    "TERMINATE_LOYAL": "원정종료(선승리)",
    "TERMINATE_EVIL": "원정종료(악승리)",
    "ASSASSIN": "암살자",
    "ASSASSIN_FAIL": "암살실패",
    "QUEST_SUCCESS": "성공",
    "QUEST_FAIL": "실패",
    "ALREADY_RESULT": "제출완료",
    "LOYAL_FAIL": "선실패불가",
    "VIVIANE": "호수의여신",
    "ORGANIZE_QUEST": "원정결과",
    "VIVIANE_LOYAL": "호수의여신(선)",
    "VIVIANE_EVIL": "호수의여신(악)",
    "LOCK_GAME": "명령처리",
}

# 버튼
BUTTONS = {
    STATUS["AVALON"]: {"type": 2, "label": STATUS["AVALON"], "style": 1, "custom_id": STATUS["AVALON"]},
    STATUS["EXPLAIN"]: {"type": 2, "label": STATUS["EXPLAIN"], "style": 2, "custom_id": STATUS["EXPLAIN"]},
    STATUS["STATUS"]: {"type": 2, "label": STATUS["STATUS"], "style": 3, "custom_id": STATUS["STATUS"]},
    STATUS["RECRUIT"]: {"type": 2, "label": STATUS["RECRUIT"], "style": 1, "custom_id": STATUS["RECRUIT"]},
    STATUS["DISMISSION"]: {"type": 2, "label": STATUS["DISMISSION"], "style": 4, "custom_id": STATUS["DISMISSION"]},
    STATUS["APPLY"]: {"type": 2, "label": STATUS["APPLY"], "style": 3, "custom_id": STATUS["APPLY"]},
    STATUS["OPTION"]: {"type": 2, "label": STATUS["OPTION"], "style": 2, "custom_id": STATUS["OPTION"]},
    STATUS["COMMENCE"]: {"type": 2, "label": STATUS["COMMENCE"], "style": 1, "custom_id": STATUS["COMMENCE"]},
    STATUS["INITIAL"]: {"type": 2, "label": STATUS["INITIAL"], "style": 4, "custom_id": STATUS["INITIAL"]},
    STATUS["PERCIVAL_MORGANA"]: {"type": 2, "label": STATUS["PERCIVAL_MORGANA"], "style": 1,
                                 "custom_id": STATUS["PERCIVAL_MORGANA"]},
    STATUS["MORDRED"]: {"type": 2, "label": STATUS["MORDRED"], "style": 3, "custom_id": STATUS["MORDRED"]},
    STATUS["OBERON"]: {"type": 2, "label": STATUS["OBERON"], "style": 2, "custom_id": STATUS["OBERON"]},
    STATUS["ANONYMOUS"]: {"type": 2, "label": STATUS["ANONYMOUS"], "style": 4, "custom_id": STATUS["ANONYMOUS"]},
    STATUS["PROPOSAL"]: {"type": 2, "label": STATUS["PROPOSAL"], "style": 1, "custom_id": STATUS["PROPOSAL"]},
    STATUS["APPROVE"]: {"type": 2, "label": STATUS["APPROVE"], "style": 1, "custom_id": STATUS["APPROVE"]},
    STATUS["REJECT"]: {"type": 2, "label": STATUS["REJECT"], "style": 4, "custom_id": STATUS["REJECT"]},
    STATUS["QUEST_SUCCESS"]: {"type": 2, "label": STATUS["QUEST_SUCCESS"], "style": 1,
                              "custom_id": STATUS["QUEST_SUCCESS"]},
    STATUS["QUEST_FAIL"]: {"type": 2, "label": STATUS["QUEST_FAIL"], "style": 4, "custom_id": STATUS["QUEST_FAIL"]},
}

# 봇 응답 범위
INTERACTION_SCOPE = {
    "공개": 0,
    "개인": 64,
}

# 봇 응답 유형
INTERACTION_CALLBACK = {
    "응답": 4,
    "ACK": 7,
}

# 역할자
ROLES = {
    "merlin": {"name": "멀린", "lawful": "loyal", "order": 1},
    "percival": {"name": "퍼시발", "lawful": "loyal", "order": 2},
    "assassin": {"name": "암살자", "lawful": "evil", "order": 1},
    "morgana": {"name": "모르가나", "lawful": "evil", "order": 2},
    "mordred": {"name": "모드레드", "lawful": "evil", "order": 4},
    "oberon": {"name": "오베론", "lawful": "evil", "order": 5},
    "lancelot_loyal": {"name": "랜슬롯(선)", "lawful": "loyal", "order": 3},
    "lancelot_evil": {"name": "랜슬롯(악)", "lawful": "evil", "order": 3},
    "guinevere": {"name": "기네비어", "lawful": "loyal", "order": 4},
    "servant1": {"name": "선의 세력1", "lawful": "loyal", "order": 5},
    "servant2": {"name": "선의 세력2", "lawful": "loyal", "order": 6},
    "servant3": {"name": "선의 세력3", "lawful": "loyal", "order": 7},
    "servant4": {"name": "선의 세력4", "lawful": "loyal", "order": 8},
    "minion1": {"name": "악의 하수인1", "lawful": "evil", "order": 6},
    "minion2": {"name": "악의 하수인2", "lawful": "evil", "order": 7},
    "minion3": {"name": "악의 하수인3", "lawful": "evil", "order": 8},
}

ROLES_REVERSE = {
    ROLES["merlin"]["name"]: "merlin",
    ROLES["percival"]["name"]: "percival",
    ROLES["assassin"]["name"]: "assassin",
    ROLES["morgana"]["name"]: "morgana",
    ROLES["mordred"]["name"]: "mordred",
    ROLES["oberon"]["name"]: "oberon",
    ROLES["lancelot_loyal"]["name"]: "lancelot_loyal",
    ROLES["lancelot_evil"]["name"]: "lancelot_evil",
    ROLES["guinevere"]["name"]: "guinevere",
    ROLES["servant1"]["name"]: "servant1",
    ROLES["servant2"]["name"]: "servant2",
    ROLES["servant3"]["name"]: "servant3",
    ROLES["servant4"]["name"]: "servant4",
    ROLES["minion1"]["name"]: "minion1",
    ROLES["minion2"]["name"]: "minion2",
    ROLES["minion3"]["name"]: "minion3"
}

# 역할자
CHIPS = {
    "avalon_chip_5_1": "avalon_chip_5_1",
    "avalon_chip_5_2": "avalon_chip_5_2",
    "avalon_chip_5_3": "avalon_chip_5_3",
    "avalon_chip_5_4": "avalon_chip_5_4",
    "avalon_chip_5_5": "avalon_chip_5_5",
    "avalon_chip_6_1": "avalon_chip_6_1",
    "avalon_chip_6_2": "avalon_chip_6_2",
    "avalon_chip_6_3": "avalon_chip_6_3",
    "avalon_chip_6_4": "avalon_chip_6_4",
    "avalon_chip_6_5": "avalon_chip_6_5",
    "avalon_chip_7_1": "avalon_chip_7_1",
    "avalon_chip_7_2": "avalon_chip_7_2",
    "avalon_chip_7_3": "avalon_chip_7_3",
    "avalon_chip_7_4": "avalon_chip_7_4",
    "avalon_chip_7_5": "avalon_chip_7_5",
    "avalon_chip_8_1": "avalon_chip_8_1",
    "avalon_chip_8_2": "avalon_chip_8_2",
    "avalon_chip_8_3": "avalon_chip_8_3",
    "avalon_chip_8_4": "avalon_chip_8_4",
    "avalon_chip_8_5": "avalon_chip_8_5",
    "avalon_chip_approve": "avalon_chip_approve",
    "avalon_chip_deny": "avalon_chip_deny",
    "avalon_chip_fail": "avalon_chip_fail",
    "avalon_chip_quest_fail": "avalon_chip_quest_fail",
    "avalon_chip_quest_success": "avalon_chip_quest_success",
    "avalon_chip_reject": "avalon_chip_reject",
    "avalon_chip_success": "avalon_chip_success",
}

# 플레이어 수에 따른 라운드별 원정대원 수
QUESTS = {
    5: {"round": [2, 3, 2, 3, 3], "evil": 2},
    6: {"round": [2, 3, 4, 3, 4], "evil": 2},
    7: {"round": [2, 3, 3, 4, 4], "evil": 3},
    8: {"round": [3, 4, 4, 5, 5], "evil": 3},
    9: {"round": [3, 4, 4, 5, 5], "evil": 3},
    10: {"round": [3, 4, 4, 5, 5], "evil": 4}
}

# 명령
COMMANDS = """
=아발론 : 가능한 모든 명령을 보여줍니다.
=이모지 : 필요한 이모지를 디스코드 서버에 등록(1회)합니다.
"""

# 아발론
AVALONS = """
설명 : 아발론 설명을 보여줍니다.
상태 : 현재 원정 상태를 보여줍니다.
원정 : 원정준비를 시작합니다.
해산 : 모집된 원정을 해산시킵니다.
"""

# 설명
EXPLAIN = """
아발론은 마피아 장르의 보드게임입니다.
플레이어는 멀린/모드레드 팀으로 나뉘어 아서왕을 위한 원정대를 꾸리게 됩니다.
총 5번의 원정 기회가 있으며 세번의 원정을 성공/실패 시키는 팀이 승리하게 됩니다.

플레이어는 번갈아 원정대장의 역할을 수행합니다.
원정대장은 각 라운드 인원수에 맞춰 원정대를 구성하며, 모든 플레이어는 원정대에 대해 찬성/반대를 투표합니다.
찬반이 동률 혹은 반대가 과반인 경우, 다음 플레이어가 원정대장이 됩니다.
5번 연속으로 원정대 구성이 실패하는 경우는 모드레드팀이 최종승리하게 됩니다.
과반수가 찬성하는 경우, 원정을 수행하며, 원정대원들은 원정의 성공/실패를 선택합니다.
이때, 모드레드팀은 원정 실패를 시킬 수 있습니다.
"""

# 모집
RECRUITS = """
참가 : 원정에 참가 신청/취소 합니다.
옵션 : 원정대 구성 옵션을 설정합니다.
시작 : 현재 참가원으로 원정을 시작합니다.
초기화 : 원정의 정보를 초기화합니다.
"""

# 옵션
OPTIONS = """
퍼/모 : 퍼시발/모르가나를 추가/제외
모드레드 : 모드레드을 추가/제외
오베론 : 오베론을 추가/제외
익명 : 투표 결과를 익명처리
‣ 모드레드/오베론이 있으면, 호수의 여신 포함
"""

# 이모지 이름 prefix
EMOJI_PREFIX = "avalon_chip_"

# 카드 이미지 prefix
CARD_PREFIX = "avalon_card_"
