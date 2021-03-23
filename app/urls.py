from django.urls import path, include
from . import views


urlpatterns = [
    path("item/", views.ItemView.as_view()),
    path("get-item/", views.ItemListView.as_view()),
    path("get-item/<int:pk>", views.ItemDetailView.as_view()),
    path("delete/<int:pk>", views.ItemDeleteView.as_view()),
    path("update/<int:pk>", views.ItemUpdateView.as_view()),
    path("trans/", views.TransPostView.as_view()),
    path("buy/", views.BuyView.as_view()),
]