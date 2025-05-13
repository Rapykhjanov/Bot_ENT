from django.db import models
from django.utils import timezone


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Название темы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название уровня")
    required_points = models.IntegerField(verbose_name="Необходимое количество баллов")
    description = models.TextField(verbose_name="Описание уровня")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name="Текст вопроса")
    image_url = models.URLField(null=True, blank=True, verbose_name="URL изображения")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    difficulty = models.CharField(max_length=50, verbose_name="Сложность")
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Уровень сложности")

    def __str__(self):
        return f"Вопрос {self.question_id} ({self.topic})"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос", related_name="answer_set")
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата и время ответа")

    def __str__(self):
        return f"Ответ на {self.question}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Hint(models.Model):
    hint_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField(verbose_name="Текст подсказки")
    image_url = models.URLField(null=True, blank=True, verbose_name="URL изображения подсказки")

    def __str__(self):
        return f"Подсказка к {self.question}"

    class Meta:
        verbose_name = "Подсказка"
        verbose_name_plural = "Подсказки"


class TestResult(models.Model):
    test_result_id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField(verbose_name="Время начала теста", default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания теста")
    correct_answers = models.IntegerField(default=0, verbose_name="Правильные ответы")
    incorrect_answers = models.IntegerField(default=0, verbose_name="Неправильные ответы")

    def __str__(self):
        return f"Результат теста {self.test_result_id}"

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"


# 👇 Новая модель: Теория по темам
class Theory(models.Model):
    theory_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание теории")

    def __str__(self):
        return f"Теория по теме {self.topic.name}"

    class Meta:
        verbose_name = "Теория"
        verbose_name_plural = "Теории"


class TrainingSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    start_time = models.DateTimeField(default=timezone.now, verbose_name="Время начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")

    def __str__(self):
        return f"Сессия тренажёра - {self.topic.name}"

    class Meta:
        verbose_name = "Сессия тренажёра"
        verbose_name_plural = "Сессии тренажёра"