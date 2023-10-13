# urls.py

from django.urls import path, include
from rest_framework import routers
from . import views

# Define the router
router = routers.DefaultRouter()

# Register the BookViewSet with the router
router.register(r'books', views.BookViewSet)

# Specify URL paths
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('books/', include(router.urls)),
    path('api-overview/', views.ApiOverview, name='api-overview'),
    path('create/', views.add_book, name='add-items'),
    path('all/', views.view_book, name='view_book'),
    path('update/<int:pk>/', views.update_book, name='update_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
]



