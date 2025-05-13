from rest_framework import serializers
from .models import (
    Question, Answer, Hint, TestResult,
    Level, Topic,
    Theory, TrainingSession
)

# Сериализатор для темы (Topic)
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


# Сериализатор для уровня (Level)
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


# Сериализатор для вопроса (Question)
class QuestionSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)  # Вложенный сериализатор для темы
    level = LevelSerializer(read_only=True)  # Вложенный сериализатор для уровня

    class Meta:
        model = Question
        fields = '__all__'


# Сериализатор для ответа (Answer)
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


# Сериализатор для подсказки (Hint)
class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = '__all__'


# Сериализатор для результата теста (TestResult)
class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'


# Сериализатор для отправки ответа на вопрос (AnswerSubmitSerializer)
class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()  # ID вопроса
    answer_text = serializers.CharField(max_length=255)  # Текст ответа


# Сериализатор для теории (Theory)
class TheorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Theory
        fields = '__all__'


# Сериализатор для тренировочной сессии (TrainingSession)
class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = '__all__'