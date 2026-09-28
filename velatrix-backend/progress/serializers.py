from rest_framework import serializers

from .models import DailyProgress, LessonProgress, QuestionReport, XPTransaction


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson",
            "status",
            "current_wrong_streak",
            "unlocked_at",
            "completed_at",
        ]
        read_only_fields = ["id", "unlocked_at", "completed_at"]


class DailyProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = ["id", "date", "lessons_completed_today", "extremal_test_used_today"]
        read_only_fields = fields


class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = ["id", "amount", "reason", "related_lesson", "created_at"]
        read_only_fields = fields


class QuestionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionReport
        fields = ["id", "question", "reason_text", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    answer = serializers.CharField()
