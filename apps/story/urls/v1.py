from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.story.views import StoryViewSet

app_name = 'story'

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')

urlpatterns = [
    path('', include(router.urls)),
]