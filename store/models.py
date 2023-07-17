from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PAYMENT_CHOICES
class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)
    class Meta:
        verbose_name_plural = "Categories"# to override "class Category" name in admin panel
    def __str__(self):
        return self.name # to show the objects name in admin panel
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])
    
class Products(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50,default="admin")
    description = models.TextField(blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)
    image = models.ImageField( upload_to="images/", default="images/default.png")
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name="product_creator", on_delete=models.CASCADE)
    created_time = models.DateTimeField( auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Products"
        ordering = ('-created_time',)
    def get_absolute_url(self):
        return reverse("store:products_detail", args=[self.slug])
    
    def get_add_to_cart_url(self):
        return reverse("store:add_to_cart",args=[self.slug])
    def get_remove_from_cart_url(self):
        return reverse("store:remove_from_cart",args=[self.slug])
    
    
    def __str__(self):
        return self.title

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.item.title
    def get_total_product_price(self):
        return self.quantity * self.item.price
    def get_total_discount_product_price(self):
        return self.quantity * self.item.discount_price
    def get_total_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price() 
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_product_price()
        else:
            return self.get_total_product_price()
    
    
class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    # for showing many to many field in admin panel:
    
    
    def get_items(self):
        return ",".join([str(p) for p in self.items.all()])
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
  
class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_country = models.CharField( max_length=255)
    shipping_zip = models.CharField(max_length=255)

    billing_address = models.CharField(max_length=255)
    billing_address2 = models.CharField(max_length=255)
    billing_country = models.CharField( max_length=255)
    billing_zip = models.CharField(max_length=255)

    payment_option = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Addresses"
