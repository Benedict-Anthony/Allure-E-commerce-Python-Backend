from django.urls import path

from lessons.views import LessonView
from products.views import CategoryListView, ProductListView 
from users.views import ConfirmAccount, UserCreateView
    
urlpatterns = [
    
    path("lessons/", LessonView.as_view()),
    path("products/", ProductListView.as_view()),
    path("category/", CategoryListView.as_view()),
    path("user/create/", UserCreateView.as_view()),
    path("user/confirm/<str:token>/", ConfirmAccount.as_view()), 

    
    
    path("lessons/<slug:slug>/", LessonView.as_view()),
    path("lessons/<slug:assets>/assets/", LessonView.as_view()),
    
    path("products/<slug:category>/category/", ProductListView.as_view()),
    path("products/search/<str:params>/", ProductListView.as_view()),
    path("products/<slug:slug>", ProductListView.as_view()),
] 