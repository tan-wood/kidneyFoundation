from django.urls import path
from .views import indexPageView, LandingPageView, LoginPageView, AboutPageView, apiPageView, apiJSONView

urlpatterns = [
    path("home/", indexPageView, name="home"),
    path("login/", LoginPageView, name="login"),
    path("about/", AboutPageView, name="about"),
    path("apitest/", apiPageView, name="apitest" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),
    path("landing/", LandingPageView, name="landing"),
    path("", LandingPageView, name="index")    
]