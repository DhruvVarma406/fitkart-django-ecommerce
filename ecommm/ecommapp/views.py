from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Product,Order,OrderItem,UserProfile,Category,Review
from django.contrib.auth.decorators import login_required
def home(request):

        products = Product.objects.all()

        q = request.GET.get('q')

        if q:
            products = products.filter(name__icontains=q)

        context = {
            'products': products
        }

        return render(request, 'home.html', context)         

def my_orders(request):

        orders = Order.objects.filter(
            user=request.user,
            complete=True
        )

        context = {
            'orders': orders
        }

        return render(
            request,
            'my_orders.html',
            context
        )

def about(request):
        return render(request, 'about.html')


def contact(request):
        return render(request, 'contact.html')


def register_user(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )

        login(request, user)
        return redirect('home')

    return render(request, 'register.html')
def logout_user(request):
        logout(request)
        return redirect('home')

def login_user(request):

        if request.method == "POST":

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('home')

        return render(request, 'login.html')

   # def display_product(request):

    #    product=Product.objects.all()
        
     #   context = {
      #      'products': product
       # }
        #return render(request,'home.html',context)

def product_detail(request, pk):

        product = get_object_or_404(Product, pk=pk)
        reviews = Review.objects.filter(
            product=product
        )

        context = {
            'product': product,
            'reviews': reviews,
        }

        return render(request, 'product_detail.html', context)
@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    if product.stock <= 0:
        return redirect('home')

    order, created = Order.objects.get_or_create(
        user=request.user,
        complete=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if order_item.quantity < product.stock:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('cart')
def cart(request):

        order, created = Order.objects.get_or_create(
            user=request.user,
            complete=False
        )

        items = order.orderitem_set.all()

        context = {
            'items': items,
            'order': order,
        }

        return render(
            request,
            'cart.html',
            context
        )
@login_required
def update_item(request, pk, action):

    product = get_object_or_404(
        Product,
        id=pk
    )

    order = Order.objects.get(
        user=request.user,
        complete=False
    )

    order_item = OrderItem.objects.get(
        order=order,
        product=product
    )

    if action == 'add':

        if order_item.quantity < product.stock:
            order_item.quantity += 1

    elif action == 'remove':

        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return redirect('cart')

def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        'profile': profile
    }

    return render(
        request,
        'profile.html',
        context
    )

def update_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.city = request.POST['city']
        profile.state = request.POST['state']
        profile.pincode = request.POST['pincode']

        profile.save()

        return redirect('profile')

    context = {
        'profile': profile
    }

    return render(
        request,
        'update_profile.html',
        context
    )

def category_products(request, category_name):

    products = Product.objects.filter(
        category__name__iexact=category_name
    )

    context = {
        'products': products
    }

    return render(
        request,
        'home.html',
        context
    )
@login_required
def checkout(request):

    order = Order.objects.get(
        user=request.user,
        complete=False
    )

    items = order.orderitem_set.all()

    for item in items:

        if item.product.stock >= item.quantity:

            item.product.stock -= item.quantity
            item.product.save()

    order.complete = True
    order.save()

    return redirect('my_orders')

def add_review(request, pk):

    product = Product.objects.get(
        id=pk
    )

    if request.method == "POST":

        rating = request.POST['rating']
        comment = request.POST['comment']

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )

    return redirect(
        'product_detail',
        pk=pk
    )