from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import HttpResponse

from users.models import CustomUser
from .token import decode_token


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
    

class ConfirmAccount(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        return Response({"msg":"Please activate your account before login in"})
    
    def post(self, request, *args, **kwargs):
        token = kwargs.get("token")
        if token:
            user = decode_token(token)
            if user:
                try:
                    new_user = CustomUser.objects.get(id=user["payload"].get("id"), email=user["payload"].get("email"))
                    new_user.is_active = True
                    new_user.save()
                    return Response({"msg":"congratulations, your account has been activated"})
                
                except CustomUser.DoesNotExist:
                    return Response({"error":"User does not exist"})
                
        return HttpResponse("Invalid Token")