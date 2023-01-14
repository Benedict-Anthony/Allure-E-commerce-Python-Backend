from dataclasses import fields
from rest_framework import serializers
from lesson.models import Lesson, Asset, Instruction
from products.models import Category, Products


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]
    
    def validate_name(self, value):
        unique_constraints = Category.objects.filter(name__iexact=value)
        if unique_constraints.exists():
            raise serializers.ValidationError(f"{value} already exist in category")
        
        return value
        
        

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True)
    # category = CategorySerializer(many=True)
    instructions = InstructionSerializer(many=True)
    # topics = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Lesson
        fields = [ "id",
                    "title",
                    "thumbnail_url",
                    "image_url",
                    "description",
                    "level",
                    "type",
                    "created",
                    "updated",
                    "category",
                    "slug",
                    "assets",
                    "instructions"
                ]

    
    def get_topics(self, obj):
        try:
            return obj.topics
        except:
            return ""
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # assets = AssetSerializer(many=True)
    class Meta:
        model = Products
        fields = ["id", 
                  "name", 
                  "description", 
                  "rating",
                  "price",
                  "product_price",
                  "product_discount",
                  "disc_perc",
                  "thumbnail_url",
                  "image_url", 
                  "slug",
                  "category",
                #   "assets"
                  ]