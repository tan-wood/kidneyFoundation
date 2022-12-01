from django.urls import path
from .views import indexPageView, SignOutPageView, LandingPageView, LoginPageView, AboutPageView, LogFoodPageView, apiJSONView, AlertsPageView, DiaryPageView, AccountPageView

urlpatterns = [
    path("home/", indexPageView, name="home"),
    path("alerts/", AlertsPageView, name="alerts"),
    path("diary/", DiaryPageView, name="diary"),
    path("account/<str:method>/", AccountPageView, name="account"),
    path("login/<str:method>/", LoginPageView, name="login"),
    path("about/", AboutPageView, name="about"),
    path("logfood/", LogFoodPageView, name="logfood" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),
    path("landing/", LandingPageView, name="landing"),
    path("signout/", SignOutPageView, name="signout" ),
    path("", LandingPageView, name="index")    
]