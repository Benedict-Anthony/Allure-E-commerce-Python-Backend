from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import HttpResponse


from users.serializer import UserCreateSerializer
# Create your views here.

class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        try:
            serilizer.save()
        except Exception as exec:
            return Response({"error":str(exec)})
       
        return Response({"msg":"success"}, status=status.HTTP_201_CREATED)
    

class ConfirmAccout(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Account Confirmed")
    
    def post(self, request, *args, **kwargs):
        token = kwargs.get("token")
        if token:
            print(token)
            return HttpResponse("Account Confirmed")