from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Lesson, Question

from .models import LessonAttempt, LessonProgress, XPTransaction
from .serializers import (
    LessonProgressSerializer,
    QuestionReportSerializer,
    SubmitAnswerSerializer,
    XPTransactionSerializer,
)
from .services import start_lesson_attempt, submit_answer

# Create your views here.


class MyProgressListView(generics.ListAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)


class MyXPHistoryView(generics.ListAPIView):
    serializer_class = XPTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return XPTransaction.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class QuestionReportCreateView(generics.CreateAPIView):
    serializer_class = QuestionReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StartLessonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id, is_published=True)
        except Lesson.DoesNotExist:
            return Response({"detail": "Dars topilmadi."}, status=404)

        attempt = start_lesson_attempt(request.user, lesson)
        return Response(
            {"attempt_id": attempt.id, "attempt_number": attempt.attempt_number}
        )


class SubmitAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, attempt_id):
        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            attempt = LessonAttempt.objects.get(
                id=attempt_id, user=request.user, result="in_progress"
            )
        except LessonAttempt.DoesNotExist:
            return Response({"detail": "Faol urinish topilmadi."}, status=404)

        try:
            question = Question.objects.get(id=serializer.validated_data["question_id"])
        except Question.DoesNotExist:
            return Response({"detail": "Savol topilmadi."}, status=404)

        result = submit_answer(
            request.user, attempt, question, serializer.validated_data["answer"]
        )
        return Response(result)
