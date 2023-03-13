from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Post
from rest_framework import status
from django.db.models import Q

from .serializers import PostSerializer
from products.serializer import ProductSerializer



class PostView(APIView):
    serializer_class = PostSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        assets = kwargs.get("assets")
        if slug:
            queryset = Post.objects.get(slug=slug)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)


        if assets:
            try:
                queryset = Post.objects.get(slug=assets)
                serializer = ProductSerializer(queryset.assets.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"data":404}, status=status.HTTP_404_NOT_FOUND)
        queryset = Post.objects.all().order_by("-created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
