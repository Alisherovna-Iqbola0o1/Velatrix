from django.contrib import admin

from .models import (
    DailyProgress,
    ExtremalTestAttempt,
    LessonAttempt,
    LessonChatMessage,
    LessonProgress,
    QuestionAttempt,
    QuestionReport,
    XPTransaction,
)

# Register your models here.


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "status", "current_wrong_streak", "completed_at")
    list_filter = ("status",)


@admin.register(LessonAttempt)
class LessonAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "attempt_number", "result", "started_at")
    list_filter = ("result",)


@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ("question", "is_correct", "answered_at")


@admin.register(LessonChatMessage)
class LessonChatMessageAdmin(admin.ModelAdmin):
    list_display = ("lesson_attempt", "sender", "order", "created_at")


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "lessons_completed_today",
        "extremal_test_used_today",
    )


@admin.register(ExtremalTestAttempt)
class ExtremalTestAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "passed", "taken_at")
    list_filter = ("passed",)


@admin.register(XPTransaction)
class XPTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "reason", "created_at")


@admin.register(QuestionReport)
class QuestionReportAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "status", "created_at")
    list_filter = ("status",)
