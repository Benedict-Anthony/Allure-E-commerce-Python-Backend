from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import HttpResponse
from users.models import CustomUser, UserProfile
from .token import decode_token

from users.serializer import GoogleAuthSerialiazer, UserCreateSerializer, UserProfileCreateSerializer, UserProfileSerializer


class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # serializer.is_active = False
           user = serializer.save()
           user.is_active = False
           user.save()

            
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
            print(user)
            if user:
                try:
                    new_user = CustomUser.objects.get(id=user["payload"].get("id"), email=user["payload"].get("email"))
                    new_user.is_active = True
                    new_user.save()
                    return Response({"msg":"congratulations, your account has been activated"})
                
                except CustomUser.DoesNotExist:
                    return Response({"error":"User does not exist"})
                
        return HttpResponse("Invalid Token")




class UserAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    def get(self, request):
       user = request.user
       try:
            profile = UserProfile.objects.get(user=user)
            serializer = self.serializer_class(profile).data
            return Response(serializer)
       except UserProfile.DoesNotExist:
           return Response({"msg": "you don't have a profile. Consider creating one"}, status=status.HTTP_404_NOT_FOUND)
       
       
       return Response({"msg":"error"})
   
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors)



            

class GoogleAuth(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthSerialiazer
    def post(self, request):
       serializer = self.serializer_class(data=request.data)
       try:
            if serializer.is_valid():
                try:
                    user = CustomUser.objects.get(email=serializer.data.get("email"), first_name=serializer.data.get("given_name"), last_name=serializer.data.get("family_name"))
                    if user:
                        return Response({"msg":"user found"}, status=status.HTTP_200_OK)
                except CustomUser.DoesNotExist:
                    if serializer.data.get("email") in CustomUser.objects.all().values_list("email", flat=True):
                        return Response({"error":"Email already exist"})
                    
                    user = CustomUser.objects.create(email=serializer.data.get("email"), first_name=serializer.data.get("given_name"), last_name=serializer.data.get("family_name"))
                    user.set_password(serializer.data.get("sub"))
                    user.save()
                    return Response({"msg":"user created"}, status=status.HTTP_201_CREATED)
       except Exception as exec:
            print(str(exec))
            return Response({"error":str(exec)})
       return Response({"error":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)