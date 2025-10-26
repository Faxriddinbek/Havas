from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.user.urls.v1', namespace='users')),
    # path('<int:car_id>/rent/', CarRentCreateAPIView.as_view(), name='rent'),
]