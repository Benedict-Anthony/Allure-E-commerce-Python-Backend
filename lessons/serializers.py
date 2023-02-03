from rest_framework import serializers
from lessons.models import Lesson, Asset, Instruction
from products.models import Products

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields =["name"]



        

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True)
    instructions = InstructionSerializer(many=True)
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
                    "slug",
                    "assets",
                    "instructions"
                ]

    
        
