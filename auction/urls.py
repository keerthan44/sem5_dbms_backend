"""pheonix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path("create/", views.create_auction),
    path("update/", views.update_auction),
    path("all/", views.get_auctions),
    path("summary/", views.get_auction_summary),
    
    path("create/item/", views.create_items),
    path("update/item/", views.update_items),
    path("get/items/auction", views.get_all_items_auction),

    path("create/bid/", views.create_bid),
    # path('signup/', views.signUp),
    # path('login/', views.login),
]
