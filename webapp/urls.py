from django.urls import path
from webapp.views import UserLoginView, home_view, logout_user, UserRegistrationView, QuestionView, AnswerView, UserPreferenceView

app_name = "webapp"

urlpatterns = [
    path("", home_view, name="home_page"),
    path('login/', UserLoginView.as_view(), name="login_page"),
    path('logout/', logout_user, name='logout'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('questions/', QuestionView.as_view(), {"pk": None} , name='questions'),
    path('questions/<int:pk>/', QuestionView.as_view(), name='question'),
    path('answer/<int:question_id>/', AnswerView.as_view() ,name='answer'),
    path('reaction/<str:reaction>/<int:answer_id>/', UserPreferenceView.as_view(), name='reaction')
]