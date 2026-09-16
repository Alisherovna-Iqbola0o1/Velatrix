from rest_framework import serializers


class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField(allow_null=True)
    course_xp = serializers.IntegerField()
    