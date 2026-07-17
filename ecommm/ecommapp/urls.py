from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path(
    'update_item/<int:pk>/<str:action>/',
    views.update_item,
    name='update_item'
     ),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path(
    'logout/',
    views.logout_user,
    name='logout'
),
    path('profile/',views.profile_view,name='profile'),
    path(
    'update_profile/',
    views.update_profile,
    name='update_profile'
),
    path(
    'category/<str:category_name>/',
    views.category_products,
    name='category_products'
),
path(
    'checkout/',
    views.checkout,
    name='checkout'
),
path(
    'add_review/<int:pk>/',
    views.add_review,
    name='add_review'
),
path(
    'thank-you/',
    views.thank_you,
    name='thank_you'
),
]

