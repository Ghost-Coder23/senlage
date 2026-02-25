from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .models import Product
from .forms import ContactForm


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f'New Contact Form Message from {name}'
            body = (
                f'Name: {name}\n'
                f'Email: {email}\n\n'
                f'Message:\n{message}'
            )

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message was sent successfully.')
            except Exception:
                messages.error(request, 'Unable to send your message right now. Please try again.')
            return redirect(f"{reverse('home')}#contact")
        messages.error(request, 'Please fill in all fields with valid information.')
        return redirect(f"{reverse('home')}#contact")

    return render(request, 'pages/home.html', {'contact_form': ContactForm()})


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
