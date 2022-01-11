from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .utils import searchProject, paginateProject
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
# Create your views here.

def projects(request):
    """
    Projects Page
    """
    # Search Function
    projects, search_query = searchProject(request)
    # Paginate Function
    projects, custom_range = paginateProject(request, projects, 3)
   
    context = {"projects": projects, "search_query": search_query, "custom_range": custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    """
    Single Project Page
    """
    project = Project.objects.get(id=pk)

    form = ReviewForm()
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()

            messages.success(request, "Your review was successfully submitted.")
            # refresh the page
            return redirect('project', pk=project.id)

    reviewers = project.reviewers

    project.get_vote_count

    context = {"project": project, "tags": project.tags.all(), "form": form, "reviewers": reviewers}
    return render(request, 'projects/singleProject.html', context)

@login_required(login_url="login")
def create_project(request):
    """
    Create New Projects
    """
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
    """
    Edit Project
    """
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
    """
    Delete Project
    """
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project was deleted successfully.")
        return redirect('account')
    context = {'object': project}
    return render(request, 'deleteTemplate.html', context)
