from const import ROLES, ROLES_REVERSE, QUESTS


class Game:
    def __init__(self, channel):
        self._channel = channel
        self._roles = {
            "loyal": [ROLES["merlin"], ROLES["servant1"], ROLES["servant2"]],
            "evil": [ROLES["assassin"], ROLES["minion1"]],
        }
        self._members = []
        self._viviane = []
        self._leader = None
        self._rounds = {
            1: {"players": QUESTS[5]["round"][0], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            2: {"players": QUESTS[5]["round"][1], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            3: {"players": QUESTS[5]["round"][2], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            4: {"players": QUESTS[5]["round"][3], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            5: {"players": QUESTS[5]["round"][4], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
        }
        self._quest_round = 0
        self._fourth_round = False
        self._expedition = False
        self._anonymous = False
        self._percival = False
        self._mordred = False
        self._oberon = False
        self._lancelot = False

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, roles):
        # 전달된 멤버 수로 선/악의 역할자 수 구하기
        # 전체 롤의 선/악 구성 딕셔너리
        loyal = []
        evil = []
        for role in ROLES:
            if ROLES[role]["lawful"] == "loyal":
                # 퍼/모 옵션이 없는 경우, 퍼시발 제외
                if role == ROLES_REVERSE[ROLES["percival"]["name"]] and not self._percival:
                    continue
                # 랜슬롯 옵션이 없는 경우, 랜슬롯 제외
                if role == ROLES_REVERSE[ROLES["lancelot_loyal"]["name"]] and not self._lancelot:
                    continue
                loyal.append(ROLES[role])
            else:
                # 퍼/모 옵션이 없는 경우, 모르가나 제외
                if role == ROLES_REVERSE[ROLES["morgana"]["name"]] and not self._percival:
                    continue
                # 모드레드 옵션이 없는 경우, 모드레드 제외
                if role == ROLES_REVERSE[ROLES["mordred"]["name"]] and not self._mordred:
                    continue
                # 오베론 옵션이 없는 경우, 오베론 제외
                if role == ROLES_REVERSE[ROLES["oberon"]["name"]] and not self._oberon:
                    continue
                # 랜슬롯 옵션이 없는 경우, 랜슬롯 제외
                if role == ROLES_REVERSE[ROLES["lancelot_evil"]["name"]] and not self._lancelot:
                    continue
                evil.append(ROLES[role])

        # 멀린팀 우선 순위대로 구성(전체 멤버 수 - 악의 세력 수)
        while len(loyal) > roles - QUESTS[roles]["evil"]:
            loyal.pop()
        # 모드레드팀 우선 순위대로 구성(전체 멤버 수 - 악의 세력 수)
        while len(evil) > QUESTS[roles]["evil"]:
            evil.pop()

        # 기존에 적용되어있던 role 초기화
        self._roles = {
            "loyal": loyal,
            "evil": evil,
        }

        # 멤버 수에 맞게 라운드별 플레이어수 변경
        self._rounds = {
            1: {"players": QUESTS[roles]["round"][0], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            2: {"players": QUESTS[roles]["round"][1], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            3: {"players": QUESTS[roles]["round"][2], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            4: {"players": QUESTS[roles]["round"][3], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
            5: {"players": QUESTS[roles]["round"][4], "members": [], "deny": 0, "vote": {"approval": [], "reject": []},
                "result": {"success": [], "fail": []}, "terminate": False},
        }

        # 멤버 수가 7명 이상인 경우, 4라운드 실패 2장 필요
        if roles >= 7:
            self._fourth_round = True
        else:
            self._fourth_round = False

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, members):
        self._members = members

    @property
    def viviane(self):
        return self._viviane

    @viviane.setter
    def viviane(self, viviane):
        self._viviane = viviane

    @property
    def leader(self):
        return self._leader

    @leader.setter
    def leader(self, leader):
        self._leader = leader

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, rounds):
        self._rounds = rounds

    @property
    def quest_round(self):
        return self._quest_round

    @quest_round.setter
    def quest_round(self, quest_round):
        self._quest_round = quest_round

    @property
    def fourth_round(self):
        return self._fourth_round

    @fourth_round.setter
    def fourth_round(self, fourth_round):
        self._fourth_round = fourth_round

    @property
    def expedition(self):
        return self._expedition

    @expedition.setter
    def expedition(self, expedition):
        self._expedition = expedition

    @property
    def anonymous(self):
        return self._anonymous

    @anonymous.setter
    def anonymous(self, anonymous):
        self._anonymous = anonymous

    @property
    def percival(self):
        return self._percival

    @percival.setter
    def percival(self, percival):
        self._percival = percival

    @property
    def mordred(self):
        return self._mordred

    @mordred.setter
    def mordred(self, mordred):
        self._mordred = mordred

    @property
    def oberon(self):
        return self._oberon

    @oberon.setter
    def oberon(self, oberon):
        self._oberon = oberon

    @property
    def lancelot(self):
        return self._lancelot

    @lancelot.setter
    def lancelot(self, lancelot):
        self._lancelot = lancelot

    def add_member(self, member):
        self._members.append(member)

    def remove_member(self, user):
        for member in self._members:
            if user == member.user:
                self._members.remove(member)
                break

    def clear_game(self):
        self._viviane = []
        self._leader = None

        5 if len(self._members) < 5 else len(self._members)
        # 멤버 수에 맞게 라운드별 플레이어수 변경
        member_count = 5 if len(self._members) < 5 else len(self._members)
        self._rounds = {
            1: {"players": QUESTS[member_count]["round"][0], "members": [], "deny": 0,
                "vote": {"approval": [], "reject": []}, "result": {"success": [], "fail": []}, "terminate": False},
            2: {"players": QUESTS[member_count]["round"][1], "members": [], "deny": 0,
                "vote": {"approval": [], "reject": []}, "result": {"success": [], "fail": []}, "terminate": False},
            3: {"players": QUESTS[member_count]["round"][2], "members": [], "deny": 0,
                "vote": {"approval": [], "reject": []}, "result": {"success": [], "fail": []}, "terminate": False},
            4: {"players": QUESTS[member_count]["round"][3], "members": [], "deny": 0,
                "vote": {"approval": [], "reject": []}, "result": {"success": [], "fail": []}, "terminate": False},
            5: {"players": QUESTS[member_count]["round"][4], "members": [], "deny": 0,
                "vote": {"approval": [], "reject": []}, "result": {"success": [], "fail": []}, "terminate": False},
        }
        self._quest_round = 0
        self._expedition = False
