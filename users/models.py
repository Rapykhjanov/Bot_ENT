# users/models.py
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    points = models.IntegerField(default=0, verbose_name="Баллы")

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"