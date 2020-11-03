from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('art/', views.art, name="art"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update-item"),
	path('process_order/', views.processOrder, name="process-order")
]
