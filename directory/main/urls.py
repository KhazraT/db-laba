from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('fam', views.fam),
    path('fam/', views.fam, name='fam'),
    path('name', views.name),
    path('name/', views.name, name='name'),
    path('otc', views.otc),
    path('otc/', views.otc, name='otc'),
    path('street', views.street),
    path('street/', views.street, name='street'),
    path('main', views.main),
    path('main/', views.main, name='main'),
]
