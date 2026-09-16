from rest_framework import serializers

from .models import Course, Section, Lesson, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    choice_text = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'order']

    def get_choice_text(self, obj):
        return obj.safe_translation_getter('choice_text', any_language=True)


class QuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()
    hint_text = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'order', 'question_type', 'question_text', 'explanation',
            'hint_text', 'difficulty', 'xp_value', 'starter_code', 'choices',
        ]

    def get_question_text(self, obj):
        return obj.safe_translation_getter('question_text', any_language=True)

    def get_explanation(self, obj):
        return obj.safe_translation_getter('explanation', any_language=True)

    def get_hint_text(self, obj):
        return obj.safe_translation_getter('hint_text', any_language=True)


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'lesson_type', 'xp_reward', 'estimated_minutes']

    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)


class SectionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'order', 'lessons']

    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)


class CourseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'slug', 'title', 'description', 'order',
            'difficulty_level', 'sections',
        ]

    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)

    def get_description(self, obj):
        return obj.safe_translation_getter('description', any_language=True)