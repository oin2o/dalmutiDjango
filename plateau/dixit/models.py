from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    delYn = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ':' + str(self.delYn)


class Game(models.Model):
    gamecode = models.CharField(max_length=6, unique=True, help_text="게임 비밀번호")
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    ingameCd = models.IntegerField(default=0, help_text="0:게임대기, 1:게임중, 2:결과확인")
    turnUser = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(default="", max_length=100)
    mastername = models.CharField(default="", max_length=10)

    def __str__(self):
        return self.gamecode + ':' + str(self.round) + ':' + str(self.ingameCd) + ':' + str(self.turnUser) \
               + ':' + self.keyword + ':' + self.mastername


class Cards(models.Model):
    name = models.CharField(default="", max_length=100, help_text="카드 이름")
    category = models.CharField(default="", max_length=100, help_text="카드 종류(폴더명)")

    def __str__(self):
        return self.name + ':' + self.category


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(default=0, help_text="순번")
    status = models.IntegerField(default=0, help_text="0:게임대기, 1:레디, 2:관전")
    storyCard = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True)
    pickusername = models.CharField(default="", max_length=10, null=True)
    point = models.IntegerField(default=0, help_text="점수")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.position) + ':' + str(self.status) \
               + ':' + str(self.storyCard) + ':' + self.pickusername + ':' + str(self.point)


class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, help_text="순번")
    check = models.IntegerField(default=0, help_text="0:unchecked, 1:checked")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) \
               + ':' + str(self.card) + ':' + str(self.order) + ':' + str(self.check)


class Honor(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    point = models.IntegerField(default=0, help_text="점수")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.round) + ':' + str(self.point)
