from django.urls import path

from cart import views


urlpatterns = [
    path('add/<offer_id>/', views.cart_add, name='cart_add'),
    path('cart_modal', views.cart_modal, name='cart_modal'),
    path('cart_submit', views.cart_submit, name='cart_submit'),
    path('remove/<offer_id>/', views.cart_remove, name='cart_remove'),
]
