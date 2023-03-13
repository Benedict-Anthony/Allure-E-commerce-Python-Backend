from rest_framework import serializers
from blog.models import Post 
from products.models import Products

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields =["name"]


class PostSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True)
    class Meta:
        model = Post
        fields = [ "id",
                    "title",
                    "thumbnail_url",
                    "image_url",
                    "description",
                    "excerpt",
                    "created",
                    "updated",
                    "slug",
                    "assets",
                ]

    
        
