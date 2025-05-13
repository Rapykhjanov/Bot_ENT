from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Question, Answer, Hint, TestResult, Level, Topic, Theory, TrainingSession
from .serializers import QuestionSerializer, AnswerSerializer, HintSerializer, TestResultSerializer, \
    LevelSerializer, TopicSerializer, AnswerSubmitSerializer, \
    TheorySerializer, TrainingSessionSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.request.query_params.get('topic', None)
        level_id = self.request.query_params.get('level', None)

        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        if level_id:
            queryset = queryset.filter(level_id=level_id)

        return queryset


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    @action(detail=True, methods=['post'])
    def check_answer(self, request, pk=None):
        answer = self.get_object()
        correct_answer = answer.question.answer_set.filter(is_correct=True).first()

        if answer.text == correct_answer.text:
            answer.is_correct = True
            answer.save()
            return Response({"message": "Правильный ответ!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Неправильный ответ!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def submit_answer(self, request):
        serializer = AnswerSubmitSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.validated_data['question_id']
            answer_text = serializer.validated_data['answer_text']

            question = Question.objects.get(question_id=question_id)

            # Добавление ответа
            answer = Answer.objects.create(question=question, text=answer_text)
            # Проверка на правильность
            correct_answer = question.answer_set.filter(is_correct=True).first()
            if correct_answer.text == answer_text:
                answer.is_correct = True
                answer.save()
                return Response({"message": "Правильный ответ!"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Неправильный ответ!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HintViewSet(viewsets.ModelViewSet):
    queryset = Hint.objects.all()
    serializer_class = HintSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    @action(detail=True, methods=['post'])
    def submit_test(self, request, pk=None):
        test_result = self.get_object()
        test_result.end_time = timezone.now()
        test_result.save()
        return Response({"message": "Результаты теста успешно отправлены!"}, status=status.HTTP_200_OK)


class TheoryViewSet(viewsets.ModelViewSet):
    queryset = Theory.objects.all()
    serializer_class = TheorySerializer

    @action(detail=True, methods=['get'])
    def get_theory(self, request, pk=None):
        theory = self.get_object()
        serializer = TheorySerializer(theory)
        return Response(serializer.data)


class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer

    @action(detail=True, methods=['get'])
    def start_training(self, request, pk=None):
        session = self.get_object()
        # Логика для начала тренировки (например, определение сессии и заданий)
        return Response({"message": f"Тренировка {session.id} начата!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def complete_training(self, request, pk=None):
        session = self.get_object()
        session.end_time = timezone.now()  # или другой логики завершения
        session.save()
        return Response({"message": f"Тренировка {session.id} завершена!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def return_to_main(self, request):
        # Логика для возврата на главную страницу
        return Response({"message": "Вы вернулись на главную страницу!"}, status=status.HTTP_200_OK)