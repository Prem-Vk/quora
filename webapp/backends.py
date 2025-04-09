from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from webapp.models import User

class CaseInsensitiveUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username.strip()
        UserModel = get_user_model()
        try:
            # Try finding by username
            user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            # Try finding by email
            try:
                user: User = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                return None

        if self.check_password(user, password):
            return user
        else:
            return None

    def check_password(self, user, password):
        return user.check_password(password)
