from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:en>", views.entry, name="entry" ),
    path('newpage/', views.newPage, name="newPage"),
    path('<str:name>/editPage', views.editPage, name="editPage"),
    path("random/", views.randomPage, name='randomPage')
]
