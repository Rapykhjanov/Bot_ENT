from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta  # Импортируем timedelta для работы с датами

# Импортируем все необходимые модели и сериализаторы
from .models import User, Subscription, Tariff, PromoCode, OfferAgreement
from .serializers import (
    SubscriptionSerializer,
    CreateSubscriptionSerializer,  # <-- Убедитесь, что импортировано
    TariffSerializer,
    ApplyPromoCodeSerializer,
    OfferAgreementSerializer
)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_serializer_class(self):  # <-- Этот метод нужно вернуть
        if self.action == 'subscribe':
            return CreateSubscriptionSerializer
        elif self.action == 'apply_promo_code':
            return ApplyPromoCodeSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """
        API для создания подписки после оплаты, основываясь на выбранном тарифе.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            tariff_id = serializer.validated_data['tariff_id']
            start_date = serializer.validated_data.get('start_date', timezone.now().date())

            try:
                user = User.objects.get(user_id=user_id)
                tariff = Tariff.objects.get(tariff_id=tariff_id, is_active=True)

                # Проверка на активную подписку
                if Subscription.objects.filter(user=user, is_active=True,
                                               end_date__gte=timezone.now().date()).exists():
                    return Response({"error": "У пользователя уже есть активная подписка."},
                                    status=status.HTTP_409_CONFLICT)

                end_date = start_date + timedelta(days=tariff.duration_days)

                subscription = Subscription.objects.create(
                    user=user,
                    tariff=tariff,  # Сохраняем тариф
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                )
                subscription_serializer = SubscriptionSerializer(subscription)
                return Response(subscription_serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"error": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)
            except Tariff.DoesNotExist:
                return Response({"error": "Тариф не найден или неактивен."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def apply_promo_code(self, request):
        """
        API для активации подписки с помощью промокода.
        """
        serializer = ApplyPromoCodeSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            promo_code_str = serializer.validated_data['promo_code']

            try:
                user = User.objects.get(user_id=user_id)

                # Проверяем, есть ли уже активная подписка у пользователя
                if Subscription.objects.filter(user=user, is_active=True,
                                               end_date__gte=timezone.now().date()).exists():
                    return Response({"error": "У пользователя уже есть активная подписка."},
                                    status=status.HTTP_409_CONFLICT)

                promo_code = PromoCode.objects.get(code=promo_code_str, is_active=True)

                # Проверки промокода
                if promo_code.expiration_date and promo_code.expiration_date < timezone.now().date():
                    return Response({"error": "Промокод истек."}, status=status.HTTP_400_BAD_REQUEST)
                if promo_code.uses_count >= promo_code.max_uses:
                    return Response({"error": "Промокод исчерпал количество использований."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Активация подписки через промокод
                start_date = timezone.now().date()
                end_date = start_date + timedelta(days=promo_code.duration_days)

                subscription = Subscription.objects.create(
                    user=user,
                    tariff=None,  # Подписка по промокоду не связана с тарифом
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                    # Можно добавить поле в Subscription для хранения использованного промокода
                    # promo_code_applied=promo_code # Если добавите Foreignkey в Subscription
                )

                # Увеличиваем счетчик использований промокода
                promo_code.uses_count += 1
                promo_code.save()

                subscription_serializer = SubscriptionSerializer(subscription)
                return Response(subscription_serializer.data, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response({"error": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)
            except PromoCode.DoesNotExist:
                return Response({"error": "Неверный или неактивный промокод."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def active_subscriptions(self, request):
        """
        Возвращает список всех активных подписок.
        """
        active_subscriptions = Subscription.objects.filter(is_active=True,
                                                           end_date__gte=timezone.now().date())  # Убедимся, что is_active = True и end_date не истекла
        serializer = SubscriptionSerializer(active_subscriptions, many=True)
        return Response(serializer.data)


class TariffViewSet(viewsets.ReadOnlyModelViewSet):  # <-- Рекомендую ReadOnlyModelViewSet
    """
    API для получения списка активных тарифов (прайс-лист).
    """
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer


class OfferAgreementViewSet(viewsets.ReadOnlyModelViewSet):  # <-- Рекомендую ReadOnlyModelViewSet
    """
    API для получения текста договора оферты.
    Возвращает самую последнюю версию договора.
    """
    queryset = OfferAgreement.objects.all().order_by('-last_updated')[:1]  # Берем только последнюю версию
    serializer_class = OfferAgreementSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"error": "Договор оферты не найден."}, status=status.HTTP_404_NOT_FOUND)