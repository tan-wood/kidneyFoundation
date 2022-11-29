from django.urls import path
from .views import indexPageView, LandingPageView, LoginPageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path('landing', ) 
]      