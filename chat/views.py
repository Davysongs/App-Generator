from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView

# Create your views here.
class ChatViewset(APIView):
    def get(self):
        return response("get chat")
    def get_queryset(self):
        return super().get_queryset()
    