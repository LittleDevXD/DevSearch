from math import perm
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated 
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

@api_view(['GET'])
def get_routes(request):

    routes = [
        {'GET': "api/projects"},
        {'GET': "api/projects/id"},
        {'POST': "api/projects/id/vote"},

        {'POST': "api/users/token"},
        {'POST': "api/users/token/refresh"},
    ]

    return Response(routes)

@api_view(['GET'])
def get_projects(request):
    """
    Many Projects JSON
    """
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_project(request, pk):
    """
    Single Project JSON
    """
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def vote_project(request, pk):
    """
    Vote Project through API
    """
    project = Project.objects.get(id=pk)
    user = request.user.profile

    # Get the data User sent
    data = request.data

    # If review, update, if not review, create
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project
    )

    review.value = data["value"]
    review.save()

    # Update vote_total and vote_ratio
    project.get_vote_count
    
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_tag(request):
    """
    Delete tags by one click while updating the project
    """
    tagID = request.data['tag']
    projectID = request.data['project']

    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)

    # Remove tag relationship with project 
    project.tags.remove(tag)

    return Response("Tag was deleted!")
