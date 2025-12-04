from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import csv
import json
from users.forms import UserUpdateForm, CustomPasswordChangeForm, CustomUserCreationForm
from users.forms import ProductForm, OrderForm
from orders.models import Order, OrderItem
from carts.models import Cart, CartItem
from products.models import Product, Category

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    period = request.GET.get("period", "all")
    today = now().date()
    start_date = None
    if period == "day":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=7)
    elif period == "month":
        start_date = today.replace(day=1)
    orders = Order.objects.all().order_by("-created_at")
    if start_date:
        orders = orders.filter(created_at__date__gte=start_date)
    total_sales = sum(order.total_amount for order in orders)
    sales_by_month = []
    for month in range(1, 13):
        monthly_orders = orders.filter(created_at__month=month)
        month_total = sum(sum(item.price * item.quantity for item in order.items.all()) for order in monthly_orders)
        sales_by_month.append(float(month_total))
    categories = Category.objects.all()
    revenue_data = []
    for category in categories:
        category_total = sum(
            item.price * item.quantity
            for order in orders
            for item in order.items.all()
            if item.product.category == category
        )
        revenue_data.append(float(category_total))
    context = {
        "users_count": User.objects.count(),
        "products_count": Product.objects.count(),
        "orders_count": orders.count(),
        "total_sales": float(total_sales),
        "period": period,
        "recent_orders": orders[:5],
        "sales_by_month_json": json.dumps(sales_by_month),
        "revenue_labels_json": json.dumps([c.name for c in categories]),
        "revenue_data_json": json.dumps(revenue_data),
    }
    return render(request, "dashboard/admin_dashboard.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def reports_view(request):
    orders = Order.objects.all().order_by("-created_at")
    total_sales = sum(sum(item.price * item.quantity for item in order.items.all()) for order in orders)
    return render(request, "dashboard/reports.html", {"orders": orders, "total_sales": total_sales})

@login_required
@user_passes_test(lambda u: u.is_staff)
def users_list(request):
    users = User.objects.all()
    return render(request, "dashboard/users.html", {"users": users})

@login_required
@user_passes_test(lambda u: u.is_staff)
def user_update_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        role = request.POST.get("role")
        user.is_staff = (role == "admin")
        user.save()
        messages.success(request, f"Role for {user.username} updated successfully!")
        return redirect("users_list")
    return render(request, "dashboard/user_role_form.html", {"user": user})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if request.user.id == user.id:
            messages.error(request, "You cannot delete your own account.")
            return redirect("users_list")
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect("users_list")
    return render(request, "dashboard/user_confirm_delete.html", {"user": user})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard_home" if user.is_staff else "shop")
    else:
        form = AuthenticationForm()
    return render(request, "dashboard/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "dashboard/signup.html", {"form": form})

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html', {'user': request.user})

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully!")
            return JsonResponse({'status': 'success', 'message': 'Settings updated successfully'})
        else:
            errors = {field: errors for field, errors in form.errors.items()}
            return JsonResponse({'status': 'error', 'message': 'Please correct the errors in the form', 'errors': errors}, status=400)
    else:
        form = UserUpdateForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'dashboard/settings.html', {'form': form, 'password_form': password_form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
        else:
            errors = json.loads(form.errors.as_json())
            return JsonResponse({'status': 'error', 'message': 'Please correct the errors in the form', 'errors': errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def user_delete(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user.id != request.user.id:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized action'}, status=403)
        user.delete()
        logout(request)
        messages.success(request, "Account deleted successfully!")
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff)
def products_list(request):
    products = Product.objects.all().select_related("category")
    categories = Category.objects.all()
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    stock = request.GET.get("stock", "")
    if search:
        products = products.filter(name__icontains=search)
    if category:
        products = products.filter(category__name=category)
    if stock == "inStock":
        products = products.filter(stock__gt=10)
    elif stock == "lowStock":
        products = products.filter(stock__gt=0, stock__lte=10)
    elif stock == "outOfStock":
        products = products.filter(stock=0)
    in_stock = products.filter(stock__gt=10).count()
    low_stock = products.filter(stock__gt=0, stock__lte=10).count()
    out_of_stock = products.filter(stock=0).count()
    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "categories": categories,
        "in_stock": in_stock,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "request": request,
    }
    return render(request, "dashboard/products.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("products_list")
    else:
        form = ProductForm()
    return render(request, "dashboard/product_form.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("products_list")
    else:
        form = ProductForm(instance=product)
    products_count = Product.objects.count()
    active_products_count = Product.objects.filter(is_active=True).count()
    low_stock_count = Product.objects.filter(stock__lte=10).count()
    recent_products = Product.objects.order_by('-created_at')[:5]
    context = {
        "form": form,
        "products_count": products_count,
        "active_products_count": active_products_count,
        "low_stock_count": low_stock_count,
        "recent_products": recent_products,
    }
    return render(request, "dashboard/product_form.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("products_list")

@login_required
def orders_list(request):
    if request.user.is_staff:
        orders = Order.objects.all().order_by("-created_at")
    else:
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "orders": page_obj,
        "total_orders": orders.count(),
        "completed": orders.filter(status="Completed").count(),
        "processing": orders.filter(status="Processing").count(),
        "pending": orders.filter(status="Pending").count(),
    }
    return render(request, "dashboard/orders.html", context)

@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Order created successfully!")
            return redirect("orders_list")
    else:
        form = OrderForm()
    return render(request, "dashboard/order_update.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully!")
            return redirect("orders_list")
    else:
        form = OrderForm(instance=order)
    return render(request, "dashboard/order_update.html", {"order": order, "form": form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect("orders_list")
    return render(request, "dashboard/order_confirm_delete.html", {"order": order})

@login_required
@user_passes_test(lambda u: u.is_staff)
def export_orders_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(["ID", "Customer", "Date", "Total", "Status"])
    for order in Order.objects.all():
        writer.writerow([
            order.id,
            order.user.username if order.user else "Guest",
            order.created_at.strftime("%Y-%m-%d"),
            sum(i.price * i.quantity for i in order.items.all()),
            order.status,
        ])
    return response

@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product")
    return render(request, "dashboard/cart.html", {"cart": cart, "items": items})

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, "Cart cleared successfully!")
    return redirect("cart_page")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect("cart_page")

@login_required
def shop_view(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    search = request.GET.get("search", "")
    selected_category = request.GET.get("category", "all")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "name")
    if search:
        products = products.filter(name__icontains=search)
    if selected_category != "all":
        products = products.filter(category__name=selected_category)
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            max_price = 1000
    if sort == "price-low":
        products = products.order_by("price")
    elif sort == "price-high":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    elif sort == "popular":
        products = products.order_by("-views")
    else:
        products = products.order_by("name")
    paginator = Paginator(products, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items_count = cart.items.count()
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        if product_id:
            product = get_object_or_404(Product, id=product_id, stock__gt=0)
            if quantity <= product.stock:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=product, defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                messages.success(request, f"Added {quantity} × {product.name} to your cart!")
            else:
                messages.error(request, f"Insufficient stock for {product.name}")
        query_params = request.GET.urlencode()
        redirect_url = f"?{query_params}" if query_params else ""
        return redirect(f"{request.path}{redirect_url}")
    context = {
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "max_price": max_price,
        "sort": sort,
        "search": search,
        "cart_items_count": cart_items_count,
    }
    return render(request, "dashboard/shop.html", context)