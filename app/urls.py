from django.urls import path, include
from . import views


urlpatterns = [
    path("item/", views.ItemView.as_view()),
    path("get_post/", views.ItemGetView.as_view()),
    path("delete/<int:pk>", views.ItemDeleteView.as_view()),
    path("update/<int:pk>", views.ItemUpdateView.as_view()),
    path("trans/", views.TransPostView.as_view()),
    path("buy/", views.BuyView.as_view()),
    # path("trans/<int:pk>", views.TransactionView.as_view()),
]