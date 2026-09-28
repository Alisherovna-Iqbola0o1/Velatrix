from rest_framework import generics

from .models import Course, Section, Question
from .permissions import IsAdminOrReadOnly
from .serializers import CourseSerializer, SectionSerializer, QuestionSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True).order_by("order")
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class SectionListView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Section.objects.filter(
            course_id=self.kwargs["course_id"], is_published=True
        ).order_by("order")


class LessonQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Question.objects.filter(
            lesson_id=self.kwargs["lesson_id"]
        ).order_by("order")
        
