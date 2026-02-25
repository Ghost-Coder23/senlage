from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from .models import Product


def home(request):
    return render(request, 'pages/home.html')


def products(request):
    products_list = Product.objects.filter(is_active=True)
    return render(request, 'pages/products.html', {'products': products_list})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'pages/product_detail.html', {'product': product})


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap_xml'))
    lines = [
        'User-agent: *',
        'Allow: /',
        '',
        f'Sitemap: {sitemap_url}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    urls = [
        {'loc': request.build_absolute_uri(reverse('home')), 'lastmod': None},
        {'loc': request.build_absolute_uri(reverse('products')), 'lastmod': None},
    ]

    for product in Product.objects.filter(is_active=True).only('pk', 'updated_at'):
        urls.append(
            {
                'loc': request.build_absolute_uri(reverse('product_detail', args=[product.pk])),
                'lastmod': product.updated_at.date().isoformat(),
            }
        )

    return render(request, 'sitemap.xml', {'urls': urls}, content_type='application/xml')
