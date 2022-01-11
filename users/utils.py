from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill

def searchProfile(request):
    # if there is no search keyword
    search_query = ''

    # if there is search keyword
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    # child model
    skills = Skill.objects.filter(name__icontains=search_query)

    # filter profiles to display
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) | 
        Q(skill__in=skills))

    return profiles, search_query

def paginateProfile(request, profiles, result):

    # Get page number 
    page = request.GET.get("page")

    # Paginator -> Projects, Result(number of objects you want to show on a page)
    paginator = Paginator(profiles, result)

    try:
        profiles = paginator.page(page)
    # if user try to enter NaN
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # if user enter exceeded page number
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

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

    return profiles, custom_range