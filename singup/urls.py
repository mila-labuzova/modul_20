from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import confirm_logout, SignUpView, upgrade_me

urlpatterns = [
    path('signup/', SignUpView.as_view(template_name='singup/signup.html'), name='signup'),
    path('login/', LoginView.as_view(template_name='singup/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='singup/logout.html'), name='logout'),
    path('confirm/logout/', confirm_logout, name='confirm_logout'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
]
