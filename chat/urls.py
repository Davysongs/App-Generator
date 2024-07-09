from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatViewset.as_view())
]
