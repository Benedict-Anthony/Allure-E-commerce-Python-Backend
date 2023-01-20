from django.urls import path
from . import views  
    
urlpatterns = [
    
    path("lessons/", views.LessonView.as_view()),
    path("products/", views.ProductListView.as_view()),
    path("category/", views.CategoryListView.as_view()),

    
    
    path("lessons/<slug:slug>/", views.LessonView.as_view()),
    path("lessons/<slug:assets>/assets/", views.LessonView.as_view()),
    
    path("products/<slug:category>/category/", views.ProductListView.as_view()),
    path("products/search/?<str:params>/", views.ProductListView.as_view()),
    path("products/<slug:slug>", views.ProductListView.as_view()),
] 