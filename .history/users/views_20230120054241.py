from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from users.serializer import UserCreateSerializer
# Create your views here.

class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        print(serilizer.data)
        return Response({"msg":"success"}, status=status.HTTP_201_CREATED)