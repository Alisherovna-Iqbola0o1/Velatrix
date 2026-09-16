import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser





LANGUAGE_CHOICES = [
    ('uz', "O'zbek"),
    ('en', "English"),
]


SECURITY_QUESTIONS_CHOICES = [
    ('mother_name', "Onangizning ismi?"),
    ('first_school', "Birinchi maktabingizning nomi?"),
    ('favourite_book', "Sevimli kitobingiz nomi?"),
    ('birth_city', "Tug'ilgan shahringiz?"),
    ('first_pet', "Birinchi uy hayvoningiz turi?"),
]



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    language_choice = models.CharField(
        max_length = 5,
        choices = LANGUAGE_CHOICES,
        default = 'uz'
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    total_xp = models.PositiveIntegerField(default=0)
    is_email_verified = models.BooleanField(default=False)

    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(blank=True, null=True)

    security_question = models.CharField(
        max_length = 30,
        choices = SECURITY_QUESTIONS_CHOICES,
        blank = True, 
        null = True
    )
    security_answer_hash = models.CharField(max_length=255, blank=True, null=True)
    is_banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username























