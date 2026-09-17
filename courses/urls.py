from django.urls import path

from .views import CourseDetailView, CourseListView, SectionListView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("<uuid:course_id>/sections/", SectionListView.as_view(), name="section-list"),
    path('lessons/<uuid:lesson_id>/questions/', LessonQuestionsView.as_view(), name='lesson-questions'),
]
