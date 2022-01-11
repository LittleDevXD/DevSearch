from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag

def searchProject(request):
    # if no search keyword, empty string
    search_query = ''

    # if search keyword
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    # tag, many to many relationship
    tags = Tag.objects.filter(name__icontains=search_query)

    # filter the projects to display
    projects = Project.objects.distinct().filter(         # distinct() - to eliminate multiples
        Q(title__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags))

    return projects, search_query

def paginateProject(request, projects, result):

    # Get page number 
    page = request.GET.get("page")

    # Paginator -> Projects, Result(number of objects you want to show on a page)
    paginator = Paginator(projects, result)

    try:
        projects = paginator.page(page)
    # if user try to enter NaN
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # if user enter exceeded page number
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # Limitation of Scrolling Bar

    # Left Index
    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    # Right Index
    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    # Range of Scrolling Bar
    custom_range = range(left_index, right_index)

    return projects, custom_range