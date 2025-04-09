from django.shortcuts import render
from django.views.generic import View
from webapp.forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout
from webapp.models import User, Question, Answer, UserPreference
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class UserLoginView(View):
    def post(self, request):

        if hasattr(request, "user"):
            if request.user.is_authenticated:
                return redirect("webapp:home_page")

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


def home_view(request):
    template_name = "home.html"
    if hasattr(request, "user"):
        if request.user.is_authenticated:
            return render(request, template_name)
    return redirect(reverse("webapp:login_page"))


def logout_user(request):
    logout(request)
    return redirect(reverse("webapp:login_page"))
