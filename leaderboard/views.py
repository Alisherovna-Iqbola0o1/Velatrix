from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from progress.models import XPTransaction
from .serializers import LeaderboardEntrySerializer

# Create your views here.


class CourseLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        transactions = (
            XPTransaction.objects
            .filter(related_lesson__section__course_id=course_id)
            .values('user__id', 'user__username', 'user__avatar')
            .annotate(course_xp=Sum('amount'))
            .order_by('-course_xp')
        )

        entries = [
            {
                'rank': index + 1,
                'username': item['user__username'],
                'avatar': item['user__avatar'],
                'course_xp': item['course_xp'],
            }
            for index, item in enumerate(transactions)
        ]

        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data)
