from django.urls import path, include
from rest_framework import routers
from .views import *


router_user_task = routers.SimpleRouter()
router_user_task.register('', TaskViewSet, basename='tasks')

router_user_data = routers.SimpleRouter()
router_user_data.register('', UserViewSet, basename='user')


urlpatterns = [
    path('login/', CustomObtainAuthToken.as_view(), name='drf-login'),

    path('tasks/', include(router_user_task.urls)),

    path('user/', include(router_user_data.urls)),

    path('get/profile', get_user, )
]
