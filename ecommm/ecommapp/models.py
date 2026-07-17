from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    price= models.FloatField()
    description=models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    def __str__(self):
        return self.name

class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    date_ordered = models.DateTimeField(auto_now_add=True)

    complete = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total

    def __str__(self):
        return str(self.id)
         

class OrderItem(models.Model):

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.id)
    
class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=10)

    address = models.TextField()

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class ShippingAddress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(
        max_length=20,
        default="COD"
    )
# uid - dhruv password-dhruv