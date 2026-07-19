from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem,Order


def home(request):
    products = Product.objects.all()
    return render(request, "store/index.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "store/product.html", {"product": product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


def cart(request):
    cart_items = CartItem.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "store/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def increase_quantity(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.quantity += 1
    item.save()
    return redirect("cart")


def decrease_quantity(request, id):
    item = get_object_or_404(CartItem, id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")


def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id)
    item.delete()
    return redirect("cart")


def checkout(request):
    cart_items = CartItem.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == "POST":
        # Clear the cart after placing the order
        cart_items.delete()

        # Redirect to order successful page
        return redirect("order_succesful")

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })
def order_succesful(request):
    return render(request,"store/order_succesful.html")