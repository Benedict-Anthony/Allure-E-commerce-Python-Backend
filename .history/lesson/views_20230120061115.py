from rest_framework.views import APIView
from rest_framework.response import Response
from lesson.models import Lesson
from rest_framework import status
from django.db.models import Q

from serializer.serializer import LessonSerializer, ProductSerializer


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
                serializer = ProductSerializer(queryset.assets.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"data":404}, status=status.HTTP_404_NOT_FOUND)
        queryset = Lesson.objects.all().order_by("-created")
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
