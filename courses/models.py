import uuid

from django.conf import settings
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Course(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=models.TextField(blank=True, null=True),
    )

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.ImageField(upload_to='course_icons/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    prerequisite_course = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='unlocks'
    )
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or str(self.id)


class Section(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='section_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or str(self.id)


class Lesson(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        theory_content=models.TextField(blank=True, null=True),
    )

    LESSON_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practice', 'Practice'),
        ('mixed', 'Mixed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField(default=0)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='mixed')
    xp_reward = models.PositiveIntegerField(default=10)
    estimated_minutes = models.PositiveIntegerField(default=10)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or str(self.id)


class Question(TranslatableModel):
    translations = TranslatedFields(
        question_text=models.TextField(),
        explanation=models.TextField(blank=True, null=True),
        hint_text=models.TextField(blank=True, null=True),
    )

    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('open_answer', 'Open Answer'),
        ('code_challenge', 'Code Challenge'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField(default=0)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    correct_answer = models.CharField(max_length=500, blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    xp_value = models.PositiveIntegerField(default=5)
    starter_code = models.TextField(blank=True, null=True)
    test_cases = models.JSONField(blank=True, null=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q{self.order} - {self.lesson}"


class Choice(TranslatableModel):
    translations = TranslatedFields(
        choice_text=models.CharField(max_length=300),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.safe_translation_getter('choice_text', any_language=True) or str(self.id)
        