from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializer import CategorySerializer, LessonSerializer, ProductSerializer
from lesson.models import Lesson, Asset, Category, Instruction
from products.models import Products
from rest_framework import status
from django.db.models import Q

class LessonView(APIView):
    serializer_class = LessonSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        assets = kwargs.get("assets")
        if slug:
            queryset = Lesson.objects.get(slug=slug)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        if assets:
            try:
                queryset = Lesson.objects.get(slug=assets)
                products = Products.objects.filter(assets__id__in=queryset.assets.all())
                print(products)
                serializer = self.serializer_class(products, many=True)
                return Response(serializer)
            except:
                pass
        queryset = Lesson.objects.all().order_by("-created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ProductListView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        category = kwargs.get("category", None)
        assets = kwargs.get("assets")
        if slug:
            try:
                queryset = Products.objects.get(slug=slug)
                serializer = self.serializer_class(queryset)  
                return Response(serializer.data)
            except Products.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
        if category:
            try:
                product = Products.objects.get(slug=category)
                queryset = Products.objects.filter(category__name=product.category.name).exclude(slug=product.slug)
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except Products.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = Products.objects.all().order_by("-created",)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def get_queryset(self):
        queryset = Category.objects.all().order_by("-id")
        
        return queryset
    