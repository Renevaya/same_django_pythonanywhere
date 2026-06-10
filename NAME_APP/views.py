from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegistrationForm

def main(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'main.html', context)

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None:
        cart = Cart.objects.create(user=request.user)
    items = cart.items.all()
    total_quantity = sum(item.quantity for item in items)
    total_price = sum(item.quantity * item.product.price for item in items)
    context = {
        'cart':cart,
        'items':items,
        'total_quantity':total_quantity,
        'total_price':total_price
    }
    return render(request, 'cart.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    data = {
        'form': form,
    }
    return render(request, 'login.html', data)

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    data = {
        'form': form,
    }
    return render(request, 'register.html', data)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, is_created = Cart.objects.get_or_create(user=request.user)

    cart_item, is_item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not is_item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')