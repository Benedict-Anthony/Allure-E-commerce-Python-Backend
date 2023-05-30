from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import HttpResponse
from users.models import CustomUser, UserProfile
from .token import decode_token
from rest_framework.parsers import FormParser, MultiPartParser
from users.serializer import (
    AddressSerializer,
    GoogleAuthSerialiazer,
    UserCreateSerializer,
    UserProfileSerializer,
)


class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    user_profile = UserProfile()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            user.is_active = False
            user.save()
            self.user_profile.user = user
            self.user_profile.save()

        except Exception as exec:
            return Response({"error": str(exec)})

        return Response({"msg": "success"}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = self.serializer_class(
            data=request.data, instance=user, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ConfirmAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"msg": "Please activate your account before login in"})

    def post(self, request, *args, **kwargs):
        token = kwargs.get("token")
        if token:
            user = decode_token(token)
            print(user)
            if user:
                try:
                    new_user = CustomUser.objects.get(
                        id=user["payload"].get("id"), email=user["payload"].get("email")
                    )
                    new_user.is_active = True
                    new_user.save()
                    return Response(
                        {"msg": "congratulations, your account has been activated"}
                    )

                except CustomUser.DoesNotExist:
                    return Response({"error": "User does not exist"})

        return HttpResponse("Invalid Token")


class UserAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            serializer = self.serializer_class(profile).data
            return Response(serializer)
        except UserProfile.DoesNotExist:
            return Response({"data": None})

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.save()
            profile.address = address
            profile.save()
            serializer = self.serializer_class(profile)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        address = UserProfile.objects.get(user=user).address
        serializer = AddressSerializer(data=request.data, instance=address)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        try:
            user = request.user
            profile = UserProfile.objects.get(user=user)
            serializer = self.serializer_class(
                data=request.data, instance=profile, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"msg": str(e)})


class GoogleAuth(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthSerialiazer
    user_profile = UserProfile()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                try:
                    user = CustomUser.objects.get(
                        email=serializer.data.get("email"),
                        first_name=serializer.data.get("given_name"),
                        last_name=serializer.data.get("family_name"),
                    )
                    if user:
                        return Response(
                            {"msg": "user found"}, status=status.HTTP_200_OK
                        )
                except CustomUser.DoesNotExist:
                    if serializer.data.get(
                        "email"
                    ) in CustomUser.objects.all().values_list("email", flat=True):
                        return Response({"error": "Email already exist"})

                    user = CustomUser.objects.create(
                        email=serializer.data.get("email"),
                        first_name=serializer.data.get("given_name"),
                        last_name=serializer.data.get("family_name"),
                    )
                    user.set_password(serializer.data.get("sub"))
                    user.save()
                    self.user_profile.user = user
                    self.user_profile.save()
                    return Response(
                        {"msg": "user created"}, status=status.HTTP_201_CREATED
                    )
        except Exception as exec:
            print(str(exec))
            return Response({"error": str(exec)})
        return Response(
            {"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
        )
