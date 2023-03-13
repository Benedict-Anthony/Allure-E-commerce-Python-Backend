from rest_framework.views import APIView
from rest_framework.response import Response
from services.models import Category
from services.serializer import BookingCreateSerializer, CategorySerializer, ServiceSerializer, BookingSerializer
from rest_framework import permissions
from rest_framework import status

class ServiceCategoryView(APIView):
    serializer_class = CategorySerializer
    def get(self, request, slug=None, book=None):
        if slug:
            queryset = Category.objects.get(slug=slug).services.all()
            if book:
                book_service = queryset.get(slug=book)
                serializer = ServiceSerializer(book_service).data
                return Response(serializer)
            serializer = ServiceSerializer(queryset, many=True).data
            return Response(serializer)
        quaryset = Category.objects.all()
        serializer = self.serializer_class(quaryset, many=True).data
        return Response(serializer)


class BookServiceView(APIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        queryset = user.bookings_set.all()
        serializer = self.serializer_class(queryset, many=True).data
        return Response(serializer)
    
    def post(self, request):
        user = request.user
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"msg":"success"}, status=status.HTTP_201_CREATED)