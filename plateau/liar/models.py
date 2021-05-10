from django.db import models


class Category(models.Model):
    categoryname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.categoryname


class Words(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.category) + ':' + self.word
