from django.db import models
from django.utils import timezone
from datetime import timedelta  # Импортируем timedelta для работы с датами


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


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    # --- ДОБАВЛЕННОЕ ПОЛЕ ---
    tariff = models.ForeignKey('Tariff', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Тариф")  # Связь с моделью Tariff
    # ----------------------
    start_date = models.DateField(verbose_name="Дата начала подписки")
    end_date = models.DateField(verbose_name="Дата окончания подписки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def save(self, *args, **kwargs):
        # Проверяем активность подписки при каждом сохранении
        if self.end_date < timezone.now().date():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Подписка пользователя {self.user.fio} до {self.end_date}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Tariff(models.Model):
    """
    Модель для хранения информации о тарифах (прайс-лист).
    """
    tariff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название тарифа")
    description = models.TextField(blank=True, verbose_name="Описание тарифа")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_days = models.IntegerField(verbose_name="Длительность (дни)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class PromoCode(models.Model):
    """
    Модель для хранения промокодов на бесплатный доступ.
    """
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    duration_days = models.IntegerField(verbose_name="Длительность (дни)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Дата истечения")
    max_uses = models.IntegerField(default=1, verbose_name="Макс. количество использований")
    uses_count = models.IntegerField(default=0, verbose_name="Количество использований")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"


class OfferAgreement(models.Model):
    """
    Модель для хранения текста договора оферты.
    Можно хранить несколько версий, но API будет выдавать последнюю.
    """
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст договора")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return f"{self.title} (обновлено: {self.last_updated.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Договор оферты"
        verbose_name_plural = "Договоры оферты"
        ordering = ['-last_updated']