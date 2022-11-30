from django.urls import path
from .views import indexPageView, LandingPageView, LoginPageView, AboutPageView

urlpatterns = [
    path("home/", indexPageView, name="landing"),
    path("login/", LoginPageView, name="login"),
    path("about/", AboutPageView, name="about"),
    path("", LandingPageView, name="index")    
]      