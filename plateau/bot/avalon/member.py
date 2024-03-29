class Member:
    def __init__(self, user) -> None:
        self._user = user
        self._role = None
        self._viviane = False
        self._can_viviane = True

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    @property
    def viviane(self):
        return self._viviane

    @viviane.setter
    def viviane(self, viviane):
        self._viviane = viviane

    @property
    def can_viviane(self):
        return self._can_viviane

    @can_viviane.setter
    def can_viviane(self, can_viviane):
        self._can_viviane = can_viviane
