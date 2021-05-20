from django.db import models


class Category(models.Model):
    categoryname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.categoryname


class Words(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category) + ':' + self.word


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    delYn = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ':' + str(self.delYn)


class Game(models.Model):
    gamecode = models.CharField(max_length=6, unique=True, help_text="게임 비밀번호")
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    ingameCd = models.IntegerField(default=0, help_text="0:게임대기, 1:단어선택, 2:설명등록, 3:투표, 4:마지막찬스 5:결과확인")
    categoryname = models.CharField(default="", max_length=100)
    word = models.CharField(default="", max_length=100)
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    turnusername = models.CharField(default="", max_length=10)
    tricksterYn = models.BooleanField(default=False)
    whistleblowerYn = models.BooleanField(default=False)
    vote = models.IntegerField(default=0, help_text="0:미선택, 1:라이어, 2:사기꾼")
    targetusername = models.CharField(default="", max_length=10)
    winner = models.CharField(default="", max_length=10)
    liarlock = models.IntegerField(default=0, help_text="0:미선택, 1:제시어, 2:배신자")
    liarkey = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.gamecode + ':' + str(self.round) + ':' + str(self.ingameCd) \
               + ':' + self.categoryname + ':' + self.word + ':' + str(self.master) + ':' + self.turnusername \
               + ':' + str(self.tricksterYn) + ':' + str(self.whistleblowerYn) + ':' + str(self.vote) \
               + ':' + self.targetusername + ':' + self.winner + ':' + str(self.liarlock) + ':' + self.liarkey


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(default="", max_length=100)
    position = models.IntegerField(default=0, help_text="순번")
    status = models.IntegerField(default=0, help_text="0:게임대기, 1:레디, 2:관전")
    categoryname = models.CharField(default="", max_length=100)
    speech1 = models.CharField(default="", max_length=500)
    speech2 = models.CharField(default="", max_length=500)
    vote = models.IntegerField(default=0, help_text="0:미선택, 1:라이어, 2:사기꾼")
    targetusername = models.CharField(default="", max_length=10)

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + self.job + ':' + str(self.position) \
               + ':' + str(self.status) + ':' + self.categoryname + ':' + self.speech1 + ':' + self.speech2 \
               + ':' + str(self.vote) + ':' + self.targetusername


class Honor(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    winYn = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.round) + ':' + str(self.winYn)
