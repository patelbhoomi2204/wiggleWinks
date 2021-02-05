from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('account/login', views.login),
    path('account/register', views.register),
    path('logout', views.logout),
    path( 'item/new', views.newItem)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
