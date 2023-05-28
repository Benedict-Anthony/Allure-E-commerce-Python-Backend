from rest_framework import serializers

from users.models import CustomUser, Address, UserProfile

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
       model = CustomUser
       fields = [
           "first_name", 
           "last_name",
           "email",
           "password",
           "phone",
        #    "gender"
        ]
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]    
        if not password:
            raise ValueError("This field is required") 
        
        if password in first_name or password in last_name or password in [1,2,3]:
            raise ValueError("password is too common")
        
        if len(password) <= 5:
            raise ValueError("password should be at least 6 character")        
        
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address 
        fields = "__all__"
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "first_name", "last_name","phone"]
        
class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields =  ["user", "address", "avatar"]


class GoogleAuthSerialiazer(serializers.Serializer):
    family_name = serializers.CharField()
    given_name = serializers.CharField()
    email = serializers.EmailField()
    sub = serializers.CharField()