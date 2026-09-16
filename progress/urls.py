from django.urls import path

from .views import (
    MyProgressListView,
    MyXPHistoryView,
    QuestionReportCreateView,
    StartLessonView,
    SubmitAnswerView,
)

app_name = "progress"

urlpatterns = [
    path("my-progress/", MyProgressListView.as_view(), name="my-progress"),
    path("my-xp-history/", MyXPHistoryView.as_view(), name="my-xp-history"),
    path(
        "report-question/", QuestionReportCreateView.as_view(), name="report-question"
    ),
    path(
        "lessons/<uuid:lesson_id>/start/",
        StartLessonView.as_view(),
        name="start-lesson",
    ),
    path(
        "attempts/<uuid:attempt_id>/submit-answer/",
        SubmitAnswerView.as_view(),
        name="submit-answer",
    ),
]
