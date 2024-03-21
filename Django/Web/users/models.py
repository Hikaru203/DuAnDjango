from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    role = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.username
    
class ProductKind(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField( null=True)
    description = models.CharField(max_length=100)
    image_name=models.CharField(max_length=100, null=True)
    kind = models.ForeignKey(ProductKind, on_delete=models.CASCADE , null=True)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.user.username + " - " + self.product.name + " - " + str(self.quantity)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    date = models.DateField()
    def __str__(self):
        return self.user.username + " - " + str(self.total)
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.order.user.username + " - " + self.product.name + " - " + str(self.quantity)
    
class Discount(models.Model):
    code = models.CharField(max_length=100)
    name= models.CharField(max_length=100,null=True)
    condition = models.IntegerField()
    kind = models.ForeignKey(ProductKind, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    money = models.IntegerField( null=True)
    quantity = models.IntegerField( null=True)
    def __str__(self):
        return self.code + " - " + self.name + " - " + str(self.condition) + " - " + self.kind.name + " - " + str(self.start_date) + " - " + str(self.end_date) + " - " + str(self.money) + " - " + str(self.quantity)
    
class Discount_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " - " + self.discount.code