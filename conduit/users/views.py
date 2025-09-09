from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import UserForm, ProfileForm
from .models import User, Profile


class Login(LoginView):
    template_name = "auth/login.html"
    next_page = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.next_page)
        return super().get(request, *args, **kwargs)


class Logout(LogoutView):
    next_page = reverse_lazy("home")


class SignUp(CreateView):
    model = get_user_model()
    fields = ["username", "email", "password"]
    template_name = "auth/signup.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # create the User object
        user = form.save(commit=False)
        # set password manually
        # as otherwise the User will be saved with unhashed password
        password = form.cleaned_data.get("password")
        user.set_password(password)
        # save the User object to the database
        user.save()
        # authenticate your user with unhashed password
        # (`authenticate` expects unhashed passwords)
        email = form.cleaned_data.get("email")
        authenticated_user = authenticate(email=email, password=password)
        # log in
        login(self.request, authenticated_user)
        return redirect(self.success_url)


class ProfileDetailView(DetailView):
    model = User
    template_name = "profile/profile_detail.html"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username", None)
        profile = get_object_or_404(User, username=username).profile
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["my_articles"] = self.object.articles.order_by('-created_at')
            context["is_following"] = (
                    self.request.user.profile.is_following(self.object)
                    and self.request.user.profile != self.object
            )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "profile/settings.html"
    success_url = reverse_lazy("settings")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        profile_form = self.form_class(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class ProfileFollowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = kwargs.get("username")
        profile_to_follow = get_object_or_404(Profile, user__username=username)
        if request.user.profile.is_following(profile_to_follow):
            request.user.profile.unfollow(profile_to_follow)
        else:
            request.user.profile.follow(profile_to_follow)

        return redirect(request.POST.get("next", "profile_detail"), username=username)
