# admin.py
from django.contrib import admin
from .models import Question, Answer, Hint, TestResult, Level, Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_id', 'name')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'text', 'topic', 'difficulty', 'subject')
    search_fields = ('text',)
    list_filter = ('topic', 'difficulty', 'subject')
    raw_id_fields = ('topic',)  # Улучшает производительность при большом количестве тем


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'question', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    raw_id_fields = ('question',)


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('hint_id', 'question', 'text')
    raw_id_fields = ('question',)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_result_id', 'start_time', 'end_time', 'correct_answers', 'incorrect_answers')
    list_filter = ('start_time', 'end_time')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_id', 'name', 'required_points', 'description')
    search_fields = ('name',)