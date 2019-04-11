from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from post.serializers.serializers import Postserializer
from rest_framework import generics, viewsets
from post.models import Post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = Postserializer
    queryset = Post.objects.all()