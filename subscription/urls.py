from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Убедитесь, что импортируете views из вашей текущей аппликации

router = DefaultRouter()

# Регистрируем ViewSet'ы для создания API-эндпоинтов
router.register(r'subscription', views.SubscriptionViewSet)  # Изменено на множественное число
router.register(r'tariffs', views.TariffViewSet)
router.register(r'offer-agreement', views.OfferAgreementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Если у вас есть другие URL'ы, добавьте их здесь
]