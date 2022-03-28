class Member:
    def __init__(self, author) -> None:
        self._author = author
        self._role = ''
        self._leader = False

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    @property
    def leader(self):
        return self._leader

    @leader.setter
    def leader(self, leader):
        self._leader = leader
