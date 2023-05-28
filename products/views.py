from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from products.models import Category, Order, OrderedItems, Products
from rest_framework import status
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from users.models import Address
from .permission import OwnerRightOnly
from products.serializer import (CategorySerializer,  
                                 OrderSerializer, 
                                 ProductSerializer)
from users.email import send_mail
    
class ProductListView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug", None)
        category = kwargs.get("category", None)
        params = kwargs.get("params")

        if slug:
            try:
                queryset = Products.available_products.get(slug=slug)
                serializer = self.serializer_class(queryset)  
                return Response(serializer.data)
            except Products.DoesNotExist:
                queryset = Products.available_products.get(slug=slug)
                serializer = self.serializer_class(queryset)  
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
        if category:
            try:
                product = Products.available_products.get(slug=category)
                queryset = Products.available_products.filter(category__name=product.category.name).exclude(slug=product.slug)
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except Products.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if params:
            products = Products.available_products.search(params)
            serializer = self.serializer_class(products, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        queryset = Products.available_products.all().order_by("-created",)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductFilterView(APIView):
    def get(self, category):
        quaryset = Products.objects.filter(category__name=category)
        serializer = ProductSerializer(quaryset, many=True).data
        return Response(serializer)
        
        
class OrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerRightOnly]
    def get(self, request):
        quaryset  = Order.objects.filter(customer=request.user)
        serializer = self.serializer_class(quaryset, many=True).data
        return Response(serializer)
    
    def post(self, request):
        user = request.user
        data = request.data
        subject = "Allure Order Confirmation"
        body = f"""
        `   Hi {user.first_name},
            Your orders has been taken. 
            We will contact you soon about the delivery processes.
            
            Please Note that delivery could take up to 24 to 48 hours!
             
            Thank you for shopping with us!!!
            
            Allure.
            """
        try:
            cartItems = data["cartItems"]
            address = data["address"]
            transaction_id = data["transaction_id"]
            address, created = Address.objects.get_or_create(**address)
            for item in cartItems:
                product = Products.available_products.get(id=item.get("id"))
                price = float(item.get("quantity")) * product.product_price
               
                ordered_item = OrderedItems.objects.create(customer=user, product=product, quantity=item.get("quantity"), price=price, transaction_id=transaction_id)
                order = Order.objects.create(customer=user, order=ordered_item, address=address, total_price=price)
                order.save()
            send_mail(user.email, subject, body)
            return Response({"message":"Your order has been taken.."}, status=status.HTTP_201_CREATED) 
        except Exception as exec:
            return Response({"msg":str(exec)})


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def get_queryset(self):
        queryset = Category.objects.all().order_by("-id")
        
        return queryset
