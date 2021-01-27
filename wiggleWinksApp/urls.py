from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('account/login', views.login),
    path('account/register', views.register),
    path('logout', views.logout),
    path( 'item/new', views.newItem)
]