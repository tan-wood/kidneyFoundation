from django.urls import path
from .views import indexPageView, LandingPageView, LoginPageView, AboutPageView, apiPageView, apiJSONView

urlpatterns = [
    path("home/", indexPageView, name="landing"),
    path("login/", LoginPageView, name="login"),
    path("about/", AboutPageView, name="about"),
    path("apitest/", apiPageView, name="apitest" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),
    path("", LandingPageView, name="index")    

]      