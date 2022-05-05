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


class EggLocation(models.Model):
    egg = models.ForeignKey(Egg, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    useYn = models.BooleanField(default=True)

    def __str__(self):
        return str(self.egg) + ':' + str(self.location) + ':' + str(self.useYn)


class Abandon(models.Model):
    eggcode = models.CharField(max_length=10, unique=True)
    useYn = models.BooleanField(default=False)

    def __str__(self):
        return self.eggcode + ':' + str(self.useYn)


class TimeData(models.Model):
    timename = models.CharField(max_length=100, help_text="시간 종류")
    timevalue = models.IntegerField(default=0, help_text="시간")

    def __str__(self):
        return self.timename + ':' + str(self.timevalue)
