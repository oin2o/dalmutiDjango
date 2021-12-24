from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    userpswd = models.CharField(default="", max_length=200)
    useYn = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ':' + self.userpswd + ':' + str(self.useYn)


class Location(models.Model):
    loctname = models.CharField(max_length=50, unique=True)
    loctnum = models.CharField(default="", max_length=2)
    useYn = models.BooleanField(default=False)

    def __str__(self):
        return self.loctname + ':' + self.loctnum + ':' + str(self.useYn)


class Egg(models.Model):
    eggname = models.CharField(max_length=50, unique=True)
    eggdesc = models.CharField(default="", max_length=200)
    useYn = models.BooleanField(default=False)

    def __str__(self):
        return self.eggname + ':' + self.eggdesc + ':' + str(self.useYn)
