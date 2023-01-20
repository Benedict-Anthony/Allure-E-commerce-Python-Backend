
from rest_framework import serializers
from products.models import Category, Products


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
        


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # assets = AssetSerializer()
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