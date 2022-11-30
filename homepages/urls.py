from django.urls import path
from .views import indexPageView, LandingPageView, LoginPageView, AboutPageView, apiPageView, apiJSONView, AlertsPageView, DiaryPageView, AccountPageView

urlpatterns = [
    path("home/", indexPageView, name="home"),
    path("alerts/", AlertsPageView, name="alerts"),
    path("diary/", DiaryPageView, name="diary"),
    path("account/", AccountPageView, name="account"),
    path("login/<str:method>/", LoginPageView, name="login"),
    path("about/", AboutPageView, name="about"),
    path("apitest/", apiPageView, name="apitest" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),
    path("landing/", LandingPageView, name="landing"),
    path("", LandingPageView, name="index")    
]