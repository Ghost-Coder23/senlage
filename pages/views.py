from django.shortcuts import get_object_or_404, render
from .models import Product


def home(request):
    return render(request, 'pages/home.html')


def products(request):
    products_list = Product.objects.filter(is_active=True)
    return render(request, 'pages/products.html', {'products': products_list})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'pages/product_detail.html', {'product': product})
