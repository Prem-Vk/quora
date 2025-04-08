from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import PermissionsMixin

class User(AbstractUser, PermissionsMixin):

    profile_photo = CloudinaryField('profile_image', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(default='', max_length=300, null=True, blank=True)
    profession = models.CharField(default=None, max_length=30)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.pk}-{self.username}'


class Question(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    question_text = models.TextField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question_slug = models.SlugField(max_length=255, editable=False, null=False, blank=False, unique=True, db_index=True)
    answer_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.answer_count}->{self.question_text}'


class Answer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preferences = models.ManyToManyField(User, through='UserPreference', related_name='preference')

    def __str__(self):
        return f'{self.content[0:100]}'

class UserPreference(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    answer_id = models.ForeignKey(Answer, on_delete=models.PROTECT)
    is_liked = models.BooleanField(null=True, blank=True)
    is_disliked = models.BooleanField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _user_preference_status(self):
        if self.is_liked:
            return "has Liked the"
        elif self.is_disliked:
            return "has Disliked the"
        return "Has no preference on"

    def __str__(self):
        return f'{self.user_id.username} {self._user_preference_status} answer: {self.answer_id}'
