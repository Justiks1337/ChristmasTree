from django.db import models

# Create your models here.

class ToyTypes(models.Model):
    """
    Виды игрушек для елки
    """

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    exp = models.IntegerField()


class User(models.Model):
    """Модель юзера"""

    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    exp = models.IntegerField()
    uuid = models.UUIDField()


class Toys(models.Model):
    """Купленные игроками игрушки"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    toy = models.ForeignKey(ToyTypes, on_delete=models.CASCADE)
    slot = models.IntegerField()



