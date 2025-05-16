# tasks/serializers.py

from rest_framework import serializers
from .models import (
    Question, Answer, Hint, TestResult,
    Level, Topic,
    Theory, TrainingSession
)

# Сериализатор для темы
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

# Сериализатор для уровня
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

# ✅ Исправленный сериализатор для вопроса
class QuestionSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

# Сериализатор для ответа
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

# Сериализатор для подсказки
class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = '__all__'

# Сериализатор для результата теста
class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

# Сериализатор для отправки ответа на вопрос
class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField(max_length=255)

# Сериализатор для теории
class TheorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Theory
        fields = '__all__'

# Сериализатор для тренировочной сессии
class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = '__all__'
