from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm

# Create your views here.

def loginUser(request):
    """
    Login User
    """
    # if page is register or login
    page = "login"

    # if user has already logged in, redirect to profiles page
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # check if user exists or not
        try:
            user = User.objects.get(username=username)
        except:
            pass

        # check if username and password matches
        user = authenticate(request, username=username, password=password)

        # login
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is incorrect!")

    context = {"page": page}
    return render(request, "users/login_registerPage.html", context)

def logoutUser(request):
    """
    Logout User
    """
    logout(request)
    messages.info(request, "User has been logged out!")
    return redirect('profiles')

def registerUser(request):
    """
    Register user
    """
    # if page is register or login
    page = "register"

    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Turn username to lowercase
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, f"User was successfully created.")

            # login user after registeration 
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "An error occurred while creating user.")

    context = {"page": page, "form": form}
    return render(request, "users/login_registerPage.html", context)

def profiles(request):
    """
    Developers Page
    """
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)

def profile(request, pk):
    """
    Single Profile Page
    """
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/profile.html", context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)
