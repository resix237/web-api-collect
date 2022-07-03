from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_collect.models import imagesModel
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'images', views.imagesView,basename="images")
router.register(r'tags', views.tagsView,basename="tags")
router.register(r'modele', views.imageModelViewSet,basename="modele")
router.register(r'model', views.imageViewModel,basename="model")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('chargement/',views.chragerImageBd ),
    path('test/',views.imageApiView.as_view() ),
]