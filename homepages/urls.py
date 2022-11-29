from django.urls import path
from .views import indexPageView, apiPageView, apiJSONView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("apitest/", apiPageView, name="apitest" ),
    path("apiJSON/", apiJSONView, name="apiJSON" ),

]      