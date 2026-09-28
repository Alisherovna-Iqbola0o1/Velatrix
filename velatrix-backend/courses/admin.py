from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Choice, Course, Lesson, Question, Section


@admin.register(Course)
class CourseAdmin(TranslatableAdmin):
    list_display = ("slug", "order", "difficulty_level", "is_published")
    list_filter = ("is_published", "difficulty_level")


@admin.register(Section)
class SectionAdmin(TranslatableAdmin):
    list_display = ("course", "order", "is_published")
    list_filter = ("is_published",)


@admin.register(Lesson)
class LessonAdmin(TranslatableAdmin):
    list_display = ("section", "order", "lesson_type", "xp_reward", "is_published")
    list_filter = ("lesson_type", "is_published")


@admin.register(Question)
class QuestionAdmin(TranslatableAdmin):
    list_display = ("lesson", "order", "question_type", "difficulty", "xp_value")
    list_filter = ("question_type", "difficulty")


@admin.register(Choice)
class ChoiceAdmin(TranslatableAdmin):
    list_display = ("question", "is_correct", "order")
