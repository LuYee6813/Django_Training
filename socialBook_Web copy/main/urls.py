from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.loginUser, name="loginUser"),
    path('logout/',views.logoutUser, name="logoutUser"),
    path('settings/',views.settings, name="settings"),
    path('post/',views.post,name="post"),
]  