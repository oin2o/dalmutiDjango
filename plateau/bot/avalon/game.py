from const import ROLES


class Game:
    def __init__(self, channel):
        self._channel = channel
        self._roles = {
            'loyal': [ROLES["merlin"], ROLES["servant1"], ROLES["servant2"]],
            'evil': [ROLES["assassin"], ROLES["minion1"]],
        }
        self._members = []
        self._rounds = 0
        self._deny = 0
        self._expedition = False
        self._anonymous = False
        self._percival = False
        self._mordred = False
        self._oberon = False

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
        self._roles = roles

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, members):
        self._members = members

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, rounds):
        self._rounds = rounds

    @property
    def deny(self):
        return self._deny

    @deny.setter
    def deny(self, deny):
        self._deny = deny

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

    def add_member(self, member):
        self._members.append(member)

    def remove_member(self, user_id):
        for member in self._members:
            if member.user_id == user_id:
                self._members.remove(member)

    def clear_game(self):
        self._roles = {
            'loyal': [ROLES["merlin"], ROLES["servant1"], ROLES["servant2"]],
            'evil': [ROLES["assassin"], ROLES["minion1"]],
        }
        self._expedition = False
        self._rounds = 0
        self._deny = 0
