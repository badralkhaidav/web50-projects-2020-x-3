from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData
from django.contrib.auth import authenticate
from django.contrib import admin
from django.contrib.auth.models import User
from authtools.forms import UserCreationForm

def store(request):
	username = request.POST.get("username")
	password = request.POST.get('passwrd')
	print('username:', username)
	user = authenticate(username=username, password=password)
	if user is not None:
    	# A backend authenticated the credentials
		data = cartData(request)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		products = Product.objects.all()
		context = {'products':products, 'cartItems':cartItems}
		return render(request, 'pizza/store.html', context)
	else:
    	# No backend authenticated the credentials
		context = {'message': 'wrong identity'}
		return render(request, 'pizza/login.html', context)

def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}

	return render(request, 'pizza/cart.html', context)

def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'pizza/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	topping_description= data['topping_description']

	print('Action:', action)
	print('Product:', productId)
	print('topping_description:', topping_description)


	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	orderItem.topping_description = topping_description

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
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def login(request):


	return render(request, 'pizza/login.html')

def register(request):

	return  render(request, 'pizza/register.html')

def success(request):
	username = request.POST.get("username")
	password = request.POST.get('passwrd')
	email = request.POST.get('email')
	print('username:', username)

	user = User.objects.create(username=username, password1=password, password2=password)
	print('username created:', username)
	return  render(request, 'pizza/login.html')

def logout(request):
	return render(request, 'pizza/login.html')
