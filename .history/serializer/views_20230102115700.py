from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializer import LessonSerializer, ProductSerializer
from lesson.models import Lesson, Asset,  Instruction
from products.models import Products
from rest_framework import status
from django.db.models import Q

class LessonView(APIView):
    serializer_class = LessonSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        if slug:
            queryset = Lesson.objects.get(slug=slug)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
            
        queryset = Lesson.objects.all().order_by("-created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProductListView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        related = kwargs.get("related", None)
        print(related)
        if slug:
            try:
                queryset = Products.objects.get(slug=slug)
                serializer = self.serializer_class(queryset)  
                return Response(serializer.data)
            except Products.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        if related:
            try:
                queryset = Products.objects.get(slug=related)
                
            except Products.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

            queryset = Products.objects.filter(category__name__icontains=queryset.category.name).exclude(slug=queryset.slug).order_by("-created",)
            if len(queryset) > 0:   
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"data":None})
        
        queryset = Products.objects.all().order_by("-created",)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryListView(ListAPIView):
    
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    
    def get_queryset(self):
        queryset = Products.objects.all().order_by("-id")
        
        return queryset
    