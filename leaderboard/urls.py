from django.urls import path

from .views import CourseLeaderboardView

app_name = 'leaderboard'

urlpatterns = [
    path('<uuid:course_id>/', CourseLeaderboardView.as_view(), name='course-leaderboard'),
]
