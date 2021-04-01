from django.urls import path, include
from . import views

urlpatterns = [
    path("item/", views.ItemView.as_view()),
    path("get-item/", views.ItemListView.as_view()),
    path("get-item/<int:pk>", views.ItemDetailView.as_view()),
    path("item-delete/<int:pk>", views.ItemDeleteView.as_view()),
    path("update/<int:pk>", views.ItemUpdateView.as_view()),
    path("trans/", views.TransPostView.as_view()),
    path("get-trans/", views.TransListView.as_view()),
    path("in-trans/<int:pk>", views.TransInDeleteView.as_view()),
    path("trans-delete/<int:pk>", views.TransDeleteView.as_view()),
    path("buy/", views.BuyView.as_view()),
    path("auth/", views.AuthorView.as_view()),
    # path("order-list/", views.OrderListView.as_view()),
    # path("order/create/", views.OrderNullView.as_view()),
    # path("order/proceed/<int:pk>/<str:action>", views.OrderUpdateView.as_view()),
]
