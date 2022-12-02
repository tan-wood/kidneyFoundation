from django.urls import path
from .views import indexPageView, SignOutPageView, LandingPageView, LoginPageView, AboutPageView, LogFoodPageView
from .views import apiJSONView, AlertsPageView, DiaryPageView, AccountPageView, PickFavoritesPageView, DiaryItemPageView, DeleteItemPageView

urlpatterns = [
    path("home/", indexPageView, name="home"),
    path("alerts/", AlertsPageView, name="alerts"),
    path("diary/", DiaryPageView, name="diary"),
    path("diary_item/<int:item_id>", DiaryItemPageView, name="diary_item"),
    path("delete_item/<int:item_id>", DeleteItemPageView, name="delete_item"),
    path("account/<str:method>/", AccountPageView, name="account"),
    path("login/<str:method>/", LoginPageView, name="login"),
    path("nextsteps/", PickFavoritesPageView, name="pickfavorites"),
    path("about/", AboutPageView, name="about"),
    path("logfood/", LogFoodPageView, name="logfood" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),
    path("landing/", LandingPageView, name="landing"),
    path("signout/", SignOutPageView, name="signout" ),
    path("", LandingPageView, name="index"),
]