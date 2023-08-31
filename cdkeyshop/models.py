from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default="Category name")

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default="Product name")
    description = models.CharField(max_length=255, null=False, blank=False, default="Product description")
    price = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, default=0.00)
    image = models.ImageField(upload_to="product_images/")
    available_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ProductsCategories(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)


class Order(models.Model):
    order_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order by {self.order_by.username} on {self.order_timestamp}'


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class TrendingProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def calculate_total(self):
        cart_products = CartProduct.objects.filter(cart=self)
        return sum(cart_product.product.price for cart_product in cart_products)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
