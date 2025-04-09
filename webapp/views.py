from django.shortcuts import render
from django.views.generic import View
from webapp.forms import UserLoginForm, UserResgistrationForm, QuestionForm
from django.contrib.auth import authenticate, login, logout
from webapp.models import User, Question, Answer, UserPreference
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.utils.text import slugify


class BaseSessionView(View):

    def check_user_already_active_session(self, request):
        if hasattr(request, "user"):
            if request.user.is_authenticated:
                return redirect("webapp:home_page")

class UserLoginView(BaseSessionView):
    def post(self, request):
        self.check_user_already_active_session(request)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user: User   = authenticate(request, username=data["username"], password=data["password"])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("webapp:home_page"))
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('invalid Login')
        else:
            return HttpResponse(form.errors)

    def get(self, request):
        template_name = "session/login.html"
        return render(request, template_name)


class UserRegistrationView(BaseSessionView):
    def post(self, request):
        self.check_user_already_active_session(request)
        registration_form = UserResgistrationForm(request.POST)
        if registration_form.is_valid():
            new_user: User = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password'])
            new_user.save()
            return redirect(reverse("webapp:login_page"))
        else:
            return render(
                request,
                "session/registration.html",
                {
                    "registration_form": registration_form,
                },
            )

    def get(self, request):
        registration_form = UserResgistrationForm()
        return render(request, "session/registration.html", {"registration_form": registration_form})


class QuestionView(BaseSessionView):
    def get(self, request, pk=None):
        if pk:
            question = Question.objects.get(pk=pk)
            answers = question.answers.all()
            return render(request, "questionindetail.html", {"question": question, "answers": answers})
        else:
            return render(request, "askaquestion.html")
    def post(self, request, pk=None):
        self.check_user_already_active_session(request)
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form: Question = question_form.save(commit=False)
            question_form.question_slug, question_form.user = slugify(question_form.question_text), request.user
            question_form.save()
            return redirect(reverse("webapp:home_page"))
        else:
            return render(request, "askaquestion.html", {"form_errors": question_form.errors})

def home_view(request):
    template_name = "home.html"
    if hasattr(request, "user"):
        if request.user.is_authenticated:
            all_questions = Question.objects.select_related("user")
            return render(request, template_name, {"all_questions": all_questions})
    return redirect(reverse("webapp:login_page"))


def logout_user(request):
    logout(request)
    return redirect(reverse("webapp:login_page"))
