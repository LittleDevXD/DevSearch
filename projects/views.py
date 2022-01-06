from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag
from .forms import ProjectForm
# Create your views here.

def projects(request):
    """
    Projects Page
    """
    projectObj = Project.objects.all()
    context = {"projects": projectObj}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    """
    Single Project Page
    """
    project = Project.objects.get(id=pk)
    context = {"project": project, "tags": project.tags.all()}
    return render(request, 'projects/singleProject.html', context)

@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    context = {"form": form}
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, "Project was created successfully.")
            return redirect('account')
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            form.save()
            messages.success(request, "Project was updated successfully.")
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project was deleted successfully.")
        return redirect('account')
    context = {'object': project}
    return render(request, 'deleteTemplate.html', context)
