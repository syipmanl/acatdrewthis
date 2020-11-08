from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestOrder
from django.core.mail import send_mail


def store(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(digital=False)
	context = {'products': products, 'cartItems':cartItems }

	return render(request, 'store/store.html', context)

def art(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.filter(digital=True)
	context = {'products': products, 'cartItems':cartItems }

	return render(request, 'store/art.html', context)

def cart(request):
	data = cartData(request)
	return render(request, 'store/cart.html', data)

def checkout(request):
	data = cartData(request)
	return render(request, 'store/checkout.html', data)


def updateItem(request): 
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)	

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				province = data['shipping']['province'],
				postalcode = data['shipping']['postalcode'],
			)

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True 
	order.save()

	return JsonResponse('Payment complete!', safe=False)
# Create your views here.


