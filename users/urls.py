from django.urls import path, include
# from django.contrib.auth.urls
from .views import *


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', invalid_verify, name='invalid_verify'),
    path('my_profile/<int:pk>', EditUser.as_view(), name='edit-user'),
    path('admin-statistic-page/', custom_page, name='dashboard-page'),

]
