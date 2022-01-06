from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Review, Tag
from .forms import ProjectForm
# Create your views here.

def projects(request):
    projectObj = Project.objects.all()
    context = {"projects": projectObj}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {"project": project, "tags": project.tags.all()}
    return render(request, 'projects/singleProject.html', context)

@login_required(login_url="login")
def create_project(request):
    context = {"form": ProjectForm()}
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url="login")
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url="login")
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/deleteTemplate.html', context)
