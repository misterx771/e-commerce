from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_list, name='products_list'),
    path('products/<slug:slug>/', views.single_product, name='single_product'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]