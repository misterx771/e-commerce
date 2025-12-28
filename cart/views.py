from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from products.models import Product


def store_cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    subtotal = Decimal('0.00')

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)

        quantity = int(item.get('quantity', 1))
        price = product.price  # Decimal
        total_price = price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'total': total_price,
            'color': item.get('color', 'Black'),
            'size': item.get('size', 'M'),
        })

        subtotal += total_price

    tax = subtotal * Decimal('0.10')  # 10%
    shipping = Decimal('50.00') if subtotal > 0 and subtotal < Decimal('500.00') else Decimal('0.00')
    total = subtotal + tax + shipping

    context = {
        'title': 'Shopping Cart',
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
        'page': 'store'
    }
    return render(request, 'store.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'quantity': 1,
            'color': 'Black',
            'size': 'M',
        }

    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart')

    return redirect('store_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart')

    return redirect('store_cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        product_id = str(product_id)

        if product_id in cart:
            if quantity > 0:
                cart[product_id]['quantity'] = quantity
            else:
                del cart[product_id]

            request.session['cart'] = cart
            messages.success(request, 'Cart updated')

    return redirect('store_cart')
