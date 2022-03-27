from const import ROLES


class Game:
    def __init__(self) -> None:
        self.members = []
        self.roles = {
            'loyal': [ROLES["merlin"]],
            'evil': [ROLES["assassin"]],
        }
        self.channel = None
        self.channel = None
        self.start = False
        self.join = False

    def recruit(self, msg):
        # 게임의 상태를 모집 상태로 변경
        self.channel = msg.channel
        self.members.append(msg.message.author)
        self.join = True

    def join_in(self, msg):
        # 플레이어를 해당 원정에 참가시킴
        self.members.append(msg.message.author)

    def lock(self):
        # 원정 모집을 마감
        self.join = False

    def start(self):
        # 원정을 시작
        self.start = True

    def end(self):
        # 원정을 시작
        self.start = False
