from rest_framework import generics

from .models import Course, Section
from .permissions import IsAdminOrReadOnly
from .serializers import CourseSerializer, SectionSerializer


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
