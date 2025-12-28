from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Category, Product, PartnerCompany, Review


def home(request):
    categories = Category.objects.all()[:4]
    featured_products = Product.objects.filter(is_featured=True)[:6]
    partners = PartnerCompany.objects.all()

    context = {
        'title': 'Home - Comfy Sloth',
        'categories': categories,
        'featured_products': featured_products,
        'partners': partners,
        'page': 'home'
    }
    return render(request, 'index.html', context)


def products_list(request):
    products = Product.objects.all()

    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)

    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    categories = Category.objects.all()

    context = {
        'title': 'Products - Comfy Sloth',
        'products': products_page,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'sort_option': sort,
        'page': 'products'
    }
    return render(request, 'products.html', context)


def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    reviews = Review.objects.filter(product=product)

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    if avg_rating is None:
        avg_rating = 0

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        'title': f'{product.name} - Comfy Sloth',
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'related_products': related_products,
        'page': 'single_product'
    }
    return render(request, 'single_product.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        from django.contrib import messages
        messages.success(request, 'Thanks for subscribing!')

    return render(request, 'index.html')
