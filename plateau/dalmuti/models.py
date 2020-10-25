from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    delYn = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ':' + str(self.delYn)


class Game(models.Model):
    gamename = models.CharField(max_length=12, unique=True)
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    ingameCd = models.IntegerField(default=0, help_text="0:게임대기, 1:게임준비, 2:조공대기, 3:게임중, 4:게임종료")
    revYn = models.BooleanField(default=False)
    revusername = models.CharField(default="", max_length=10)
    drawusername = models.CharField(default="", max_length=10)
    hideCardCnt = models.IntegerField(default=5, help_text="카드 개수 숨김 구간")
    turnUser = models.ForeignKey(User, on_delete=models.CASCADE)
    lastCard = models.IntegerField(default=0, help_text="오픈 카드")
    lastCardCnt = models.IntegerField(default=0, help_text="오픈 카드 개수")
    lastJokerCnt = models.IntegerField(default=0, help_text="오픈 조커 개수")
    pickHonorYn = models.BooleanField(default=True, help_text="평민 미난입여부")
    nextgamename = models.CharField(default="", max_length=12, help_text="평민 난입시 게임")
    image = models.IntegerField(default=0, help_text="0:K무티, 1:D&D, 2:달무티")

    def __str__(self):
        return self.gamename + ':' + str(self.round) + ':' + str(self.ingameCd) \
               + str(self.revYn) + ':' + self.revusername + ':' + self.drawusername \
               + str(self.hideCardCnt) + str(self.turnUser) \
               + ':' + str(self.lastCard) + ':' + str(self.lastCardCnt) + ':' + str(self.lastJokerCnt) \
               + ':' + str(self.pickHonorYn) + ':' + self.nextgamename + ':' + str(self.image)


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    autopassYn = models.BooleanField(default=False)
    position = models.IntegerField(default=0, help_text="계급")
    cardTotCnt = models.IntegerField(default=0, help_text="보유 카드 총 개수")
    jokerCnt = models.IntegerField(default=0, help_text="조커 카드 개수")
    status = models.IntegerField(default=0, help_text="0:게임대기, 1:조공대기, 2:게임중")
    taxYn = models.BooleanField(default=False)
    nextPosition = models.IntegerField(default=0, help_text="다음계급")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + str(self.autopassYn) + ':' + str(self.position) \
               + ':' + str(self.cardTotCnt) + ':' + str(self.jokerCnt) + ':' + str(self.status) \
               + ':' + str(self.taxYn) + ':' + str(self.nextPosition)


class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.IntegerField(default=0, help_text="보유 카드")

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.card)


class Honor(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.IntegerField(default=0, help_text="게임 진행 라운드")
    gamerTotCnt = models.IntegerField(default=0, help_text="게임 참가자 인원수")
    prePosition = models.IntegerField(default=0, help_text="이전계급")
    position = models.IntegerField(default=0, help_text="계급")
    revYn = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game) + ':' + str(self.user) + ':' + str(self.round) \
               + ':' + str(self.gamerTotCnt) + ':' + str(self.prePosition) \
               + ':' + str(self.position) + ':' + str(self.revYn)
