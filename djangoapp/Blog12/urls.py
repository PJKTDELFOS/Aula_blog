from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='Blog12'

urlpatterns = [
    path('', views.Postlistview.as_view(),name='index'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(),name='post'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(),name='page'),
    path('created_by/<int:author_pk>/', views.CreatedbyListvView.as_view(),name='created_by'),
    path('category/<slug:slug>/', views.CategoryListvView.as_view(),name='category'),
    path('tag/<slug:slug>/', views.TagListvView.as_view(),name='tag'),
    path('search/', views.SearchView.as_view(),name='search'),
]