from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'topics', views.TopicViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'hints', views.HintViewSet)
router.register(r'test_results', views.TestResultViewSet)
router.register(r'levels', views.LevelViewSet)
router.register(r'theories', views.TheoryViewSet)
router.register(r'training_sessions', views.TrainingSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]