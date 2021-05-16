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
    ingameCd = models.IntegerField(default=0, help_text="0:게임대기, 1:단어선택, 2:설명등록, 3:투표, 4:결과확인")
    categoryname = models.CharField(default="", max_length=100)
    word = models.CharField(default="", max_length=100)
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    turnusername = models.CharField(default="", max_length=10)
    tricksterYn = models.BooleanField(default=False)
    whistleblowerYn = models.BooleanField(default=False)

    def __str__(self):
        return self.gamecode + ':' + str(self.round) + ':' + str(self.ingameCd) \
               + ':' + self.categoryname + ':' + self.word + ':' + str(self.master) + ':' + self.turnusername \
               + ':' + str(self.tricksterYn) + ':' + str(self.whistleblowerYn)


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.CharField(default="", max_length=100)
    position = models.IntegerField(default=0, help_text="순번")
    status = models.IntegerField(default=0, help_text="0:게임대기, 1:레디, 2:관전")
    categoryname = models.CharField(default="", max_length=100)
    vote = models.IntegerField(default=0, help_text="0:미선택, 1:사기꾼, 2:배신자")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + self.job + ':' + str(self.position) \
               + ':' + str(self.status) + ':' + self.categoryname + ':' + str(self.vote)


class Honor(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    winYn = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.round) + ':' + str(self.winYn)
