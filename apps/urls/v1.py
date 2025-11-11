from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.user.urls.v1', namespace='users')),
    path('product/', include('apps.product.urls.v1', namespace='product')),
    path('story/', include('apps.story.urls.v1', namespace='story')),
]