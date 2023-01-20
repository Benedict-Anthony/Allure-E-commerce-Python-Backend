from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from users.serializer import UserCreateSerializer
# Create your views here.

class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serilizer = self.serializer_class(data=request.data)
        try:
            serilizer.is_valid(raise_exception=True)
            serilizer.save()
        except Exception as exec:
            # print(exec)
            return Response({"error":exec})
       
        return Response({"msg":"success"}, status=status.HTTP_201_CREATED)