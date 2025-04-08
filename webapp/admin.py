from django.contrib import admin
from webapp.models import User, Question, Answer, UserPreference

admin.register(User)
admin.register(Question)
admin.register(Answer)
admin.register(UserPreference)
