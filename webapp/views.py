from django.shortcuts import render
from django.views.generic import View
from webapp.forms import UserLoginForm, UserResgistrationForm, QuestionForm, AnswerForm
from django.contrib.auth import authenticate, login, logout
from webapp.models import User, Question, Answer, UserPreference
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.utils.text import slugify
from django.db import transaction


class BaseSessionView(View):
    def check_user_already_active_session(self, request):
        if hasattr(request, "user"):
            if request.user.is_authenticated:
                return redirect("webapp:home_page")

class UserLoginView(BaseSessionView):
    """_summary_
    User login view:
        - show login page to user.
        - Autheticate and login user.
    """
    def post(self, request):
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
        self.check_user_already_active_session(request)
        template_name = "session/login.html"
        return render(request, template_name)


class UserRegistrationView(BaseSessionView):
    """_summary_
        - user sign up page.
        - Registration of a user.
    """
    def post(self, request):
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
        self.check_user_already_active_session(request)
        registration_form = UserResgistrationForm()
        return render(request, "session/registration.html", {"registration_form": registration_form})


class QuestionView(BaseSessionView):
    """_summary_
        - GET - Show a question with all answers and like,unlike count.
        - POST - To submit a question.
    """
    def get(self, request, pk=None):
        if pk:
            question = Question.objects.get(pk=pk)
            answers = question.answers.select_related("user").order_by('created_at').all()
            user_already_answered = Answer.objects.filter(
                user=request.user, question=question
            ).exists()
            return render(
                request,
                "questionindetail.html",
                {
                    "question": question,
                    "answers": answers,
                    "answered_by_user": user_already_answered,
                    "user_owned_question": request.user == question.user,
                },
            )
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


class AnswerView(BaseSessionView):
    """
    - get a answer page.
    - Submit a answer for a particular question.
    """
    def get(self, request, question_id=None):
        question = Question.objects.values("question_text", "description" ,"pk").get(pk=question_id)
        return render(request, "writeaanswer.html", {"question": question})

    def post(self, request, question_id=None):
        print("HIT TOH HUAAA HAI BHAIII")
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            with transaction.atomic():
                question_id = answer_form.cleaned_data.pop("question_id")
                question = Question.objects.get(pk=question_id)
                answer: Answer = answer_form.save(commit=False)
                answer.user, answer.question = request.user, question
                answer.save()
                question.answer_count += 1
                question.save()
            return redirect(reverse("webapp:question",  kwargs={"pk": question_id}))
        else:
            print(answer_form.errors)
            return HttpResponse(answer_form.errors)

def home_view(request):
    """_summary_
        Home page with all the questions asked by every users, with answer count.
    """
    template_name = "home.html"
    if hasattr(request, "user"):
        if request.user.is_authenticated:
            all_questions = Question.objects.select_related("user")
            return render(request, template_name, {"all_questions": all_questions})
    return redirect(reverse("webapp:login_page"))


def logout_user(request):
    """_summary_
        logout a user.
    """
    logout(request)
    return redirect(reverse("webapp:login_page"))


class UserPreferenceView(BaseSessionView):
    """_summary_
    View to handle to like & dislike for each answer.
    """
    LIKE, DISLIKE = "like", "dislike"

    def _update_like_dislike(self, preference: UserPreference, condition, opposite_condition):
        updated_fields = ['updated_at']
        if not getattr(preference, condition):
            setattr(preference, condition, True)
            updated_fields.append(condition)
        if getattr(preference, opposite_condition):
            setattr(preference, opposite_condition, False)
            updated_fields.append(opposite_condition)
        preference.save(update_fields=updated_fields)

    def get(self, request, reaction, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        preference, created = UserPreference.objects.get_or_create(user=request.user, answer=answer)
        if created:
            setattr(preference, reaction, True)
            preference.save(update_fields=[reaction, "updated_at"])
        else:
            if reaction == self.LIKE:
                self._update_like_dislike(preference, self.LIKE, self.DISLIKE)
            elif reaction == self.DISLIKE:
                self._update_like_dislike(preference, self.DISLIKE, self.LIKE)
        return redirect(reverse("webapp:question",  kwargs={"pk": answer.question.pk}))
