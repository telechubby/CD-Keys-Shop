from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from cdkeyshop.forms import *
from cdkeyshop.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Replace with your actual URL
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            # You can perform additional actions like logging in the user after registration
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not logged in

    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_product, cart_product_created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if not cart_product_created:
        # Product already in the cart, you might want to update quantity or other properties here
        pass

    return redirect('index')  # Redirect to your product list page


def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.products.remove(product)
    return redirect('index')  # Redirect to your cart page


def load_cart_contents(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'})

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = cart.cartproduct_set.all()  # Get all cart products associated with the cart

    cart_contents = []

    for cart_product in cart_products:
        product_info = {
            'id': cart_product.product.id,
            'name': cart_product.product.name,
            'price': cart_product.product.price,
            'quantity': 1,  # You might want to adjust this based on your logic
        }
        cart_contents.append(product_info)

    total = cart.calculate_total()

    response_data = {
        'cart_contents': cart_contents,
        'total': total,
    }

    return JsonResponse(response_data)


def index(request):
    trending_products = TrendingProduct.objects.select_related('product').all()
    available_products = Product.objects.filter(available_stock__gt=0)
    return render(request, 'index.html', {'trending_produ'
                                          'cts': trending_products, 'available_products': available_products})

