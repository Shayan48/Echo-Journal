# blog/urls.py
from django.urls import path
from . import views

app_name = 'blogs'  # ✅ THIS IS VERY IMPORTANT

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('add/', views.add_blog, name='add_blog'),
     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('<int:id>/', views.blog_detail, name='detail'),  # Updated to use 'id' instead of 'slug'
    path("category/<slug:category_slug>/", views.blog_list, name="category"),

]
