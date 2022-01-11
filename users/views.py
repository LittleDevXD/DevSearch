from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfile, paginateProfile

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
            return redirect(request.GET["next"] if next in request.GET else "profiles")
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
            return redirect("edit-profile")
        else:
            messages.error(request, "An error occurred while creating user.")

    context = {"page": page, "form": form}
    return render(request, "users/login_registerPage.html", context)

def profiles(request):
    """
    Developers Page
    """
    # Search Function
    profiles, search_query = searchProfile(request)

    # Paginate Function 
    profiles, custom_range = paginateProfile(request, profiles, 3)

    context = {"profiles": profiles, "search_query":search_query, "custom_range": custom_range}
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
    """
    My Account view
    """
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)

@login_required(login_url="login")
def editProfile(request):
    """
    Edit my profile
    """
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {"form": form}
    return render(request, "users/editProfile.html", context)

@login_required(login_url="login")
def createSkill(request):
    """
    Create a new skill
    """
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = profile
            skill.save()
            messages.success(request, "Skill was created successfully.")
            return redirect("account")

    context = {"form":form}
    return render(request, "users/skillForm.html", context)

@login_required(login_url="login")
def updateSkill(request, pk):
    """
    Update skill
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully.")
            return redirect("account")

    context = {"form":form}
    return render(request, "users/skillForm.html", context)

@login_required(login_url="login")
def deleteSkill(request, pk):
    """
    Delete Skill
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully.")
        return redirect("account")
    context = {"object": skill}
    return render(request, "deleteTemplate.html", context)

@login_required(login_url="login")
def inbox(request):
    """
    Inbox 
    """
    profile = request.user.profile

    messages = profile.messages.all()
    unreadCount = profile.messages.filter(is_read=False).count()

    context = {"inboxes":messages, "unreadCount":unreadCount}
    return render(request, "users/inbox.html", context)

@login_required(login_url="login")
def viewMessage(request, pk):
    """
    Read Message
    """
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    # Message has been read
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {"message":message}
    return render(request, "users/message.html", context)

def sendMessage(request, pk):
    """
    Send Message
    """
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # if user is logged in, sender is user
    # if not sender is none
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            # Recipiend and Sender
            message.recipient = recipient
            message.sender = sender
            # If there is logged in user 
            # Use its profile name and email
            if request.user.is_authenticated:
                message.name = sender.name
                message.email = sender.email
            # save
            messages.success(request, "Your message was sent successfully!")
            message.save()


    context = {"form": form, "recipient":recipient}
    return render(request, "users/message_form.html", context)
