from django.urls import path
from webapp.views import UserLoginView, home_view, logout_user

app_name = "webapp"

urlpatterns = [
    path("", home_view, name="home_page"),
    path('login/', UserLoginView.as_view(), name="login_page"),
    path('logout/', logout_user, name='logout')
]