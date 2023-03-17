from rest_framework import serializers
from products.models import Category, Order, OrderedItems, Products
from users.models import CustomUser
from users.serializer import AddressSerializer


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
                  "size",
                  "thumbnail_url",
                  "image_url", 
                  "slug",
                  "category",
                #   "assets"
                  ]
        
        
# OERDER SERIALIZERS

class OrderedProduct(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "name", "product_price", "image_url"]
class OrderItemsSerializer(serializers.ModelSerializer):
    product = OrderedProduct()
    class Meta:
        model = OrderedItems
        fields =["id", "customer", "product","quantity","price", "transaction_id",  ]
        # exclude =  ["id"]
        
        
class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ "email", "name"]




class OrderSerializer(serializers.ModelSerializer):
    order = OrderItemsSerializer()
    address = AddressSerializer()
    class Meta:
        model = Order
        fields = "__all__"
    

