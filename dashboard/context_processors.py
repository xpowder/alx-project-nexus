from carts.models import Cart


def cart_context(request):
    """Add cart count to all templates"""
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = cart.items.count()
    return {
        'cart_items_count': cart_items_count,
    }

