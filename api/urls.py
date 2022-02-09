from django import views
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Simple JSON web token
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.get_routes),
    path('projects/', views.get_projects),
    path('projects/<str:pk>', views.get_project),
    path('projects/<str:pk>/vote/', views.vote_project),

    path('remove-tag/', views.delete_tag),
    
]