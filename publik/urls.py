from services.views import BookServiceUpdateView, ServiceCategoryView, BookServiceView
from users import views
from django.urls import path

from blog.views import PostView
from products.views import CategoryListView, OrderView, ProductListView,ProductFilterView
from users.views import ConfirmAccount, GoogleAuth, UserAccountView, UserCreateView
    
urlpatterns = [
    
    path("posts/", PostView.as_view()),
    path("posts/<slug:slug>/", PostView.as_view()),
    path("posts/<slug:assets>/assets/", PostView.as_view()),
    
    
    path("user/create/", UserCreateView.as_view()),
    path("user/comfirm/<str:token>/", ConfirmAccount.as_view()), 
    path("user/account/", UserAccountView.as_view()),
    path("user/google/", GoogleAuth.as_view()),


    path("user/orders/", OrderView.as_view()),
    
    path("category/", CategoryListView.as_view()),
    
    
    path("products/", ProductListView.as_view()),
    path("products/<slug:category>/category/", ProductListView.as_view()),
    path("products/search/<str:params>/", ProductListView.as_view()),
    path("products/<slug:slug>", ProductListView.as_view()),
    path("product/filter/<str:category>/", ProductFilterView.as_view()),
    
    path("services/", ServiceCategoryView.as_view()),
    path("user/bookings/", BookServiceView.as_view()),
    path("user/bookings/<slug:slug>/update/", BookServiceUpdateView.as_view()),
    path("services/<slug:slug>/", ServiceCategoryView.as_view()),
    path("services/<slug:slug>/<slug:book>/", ServiceCategoryView.as_view()),
] 