from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser, PermissionsMixin):

    profile_photo = CloudinaryField("profile_image", null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(default="", max_length=300, null=True, blank=True)
    profession = models.CharField(default=None, max_length=30, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.pk}-{self.username}"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question_text = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_slug = models.SlugField(
        max_length=255,
        editable=False,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    answer_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.answer_count}->{self.question_text}"


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="answers")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.content[0:100]}"


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)
    reaction = models.BooleanField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _user_preference_status(self):
        if self.is_liked:
            return "has Liked the"
        elif self.is_disliked:
            return "has Disliked the"
        return "Has no preference on"

    def __str__(self):
        return f"{self.user.username} {self._user_preference_status} answer: {self.answer}"
