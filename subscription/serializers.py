from rest_framework import serializers
from django.utils import timezone
from .models import Subscription, User, Tariff, PromoCode, OfferAgreement  # Добавили импорт новых моделей


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # --- ДОБАВЛЕННОЕ ПОЛЕ ---
    tariff_name = serializers.CharField(source='tariff.name', read_only=True)  # Выводим название тарифа
    # ----------------------

    class Meta:
        model = Subscription
        fields = '__all__'
        # Если вы добавили 'tariff_name', то fields = '__all__' будет включать его.
        # Если не хотите, то явно перечислите: fields = ['subscription_id', 'user', 'tariff', 'tariff_name', 'start_date', 'end_date', 'is_active']


class CreateSubscriptionSerializer(serializers.Serializer):
    """
    Сериализатор для создания подписки через оплату.
    Теперь принимает tariff_id, чтобы бэкенд рассчитал end_date.
    """
    user_id = serializers.IntegerField(required=True)
    tariff_id = serializers.IntegerField(required=True)  # <-- Добавили
    start_date = serializers.DateField(required=False, default=timezone.now().date())


class TariffSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Тарифов.
    """

    class Meta:
        model = Tariff
        fields = '__all__'


class ApplyPromoCodeSerializer(serializers.Serializer):
    """
    Сериализатор для активации подписки с помощью промокода.
    """
    user_id = serializers.IntegerField(required=True)
    promo_code = serializers.CharField(required=True, max_length=50)


class OfferAgreementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Договора оферты.
    """

    class Meta:
        model = OfferAgreement
        fields = '__all__'