from django.urls import path

from .views import ImageCreateView

urlpatterns = [
    path('create/', ImageCreateView.as_view())
]
