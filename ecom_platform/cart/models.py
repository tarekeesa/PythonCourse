from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return str(self.user.username)  # Updated for string conversion of user object

    def get_total_quantity(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def get_total_price(self):
        return float(sum(item.get_total_price() for item in self.cartitem_set.all()))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Price at time of adding to cart
    variant = models.CharField(max_length=100, blank=True)  # Optional product variant
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(f'{self.product.title} quanitity {self.quantity}')  # Updated for string conversion of user object

    def get_total_price(self):
        total_price = self.quantity * self.price
        total_price -= self.discount_amount
        total_price -= (total_price * self.discount_percentage) / 100
        return total_price

    def price_after_discount(self):
        """Calculate price after discount for a single unit."""
        discounted_price = self.price - self.discount_amount - (self.price * self.discount_percentage / 100)
        return discounted_price
