from django.db import models
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MaxLengthValidator,
                                    MinLengthValidator)
from django.shortcuts import redirect
from MainPart.models import CustomUser
from django import forms
# Create your models here.


class Producer(models.Model):
    name = models.CharField(max_length=40, blank=False)
    country = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.name

    @staticmethod
    def _get_all_producers(self):
        return Producer.objects.all().get('name')


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    @staticmethod
    def _get_all_categories(self):
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', blank=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    discount = models.IntegerField(null=True, validators=[MaxValueValidator(80)])

    def __str__(self):
        return self.name


class Rate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    description = models.TextField(max_length=200)

    def __str__(self):
        return str(self.rate)


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def add_to_cart(self, id_item):
        '''
            In this function we have to add objects like product to our order
            We have to make additional url to each add and remove
        '''
        product = Product.objects.get(id=id_item)
        try:
            ordered_item = OrderItem.objects.get(product=product, order=self)
            ordered_item.quantity += 1
            ordered_item.save()
        except OrderItem.DoesNotExist:
            new_order = OrderItem.objects.create(product=product,
                                                 order=self,
                                                 quantity=1)
            new_order.save()

    def remove_from_cart(self, id_item):
        '''
            In this function we have to remove objects like product to our order
            We have to make additional url to each add and remove
        '''
        product = Product.objects.get(id=id_item)
        try:
            ordered_item = OrderItem.objects.get(product=product, order=self)
            ordered_item.quantity -= 1
            ordered_item.save()
        except OrderItem.DoesNotExist:
            ordered_item.delete()
            return redirect('information')

    def __str__(self):
        return str(self.id)

    def get_total(self):
        value = 0
        ordered_items = OrderItem.objects.get(order=self)

        for item in ordered_items:
            print(item.quantity)

    def get_object(self):
        return self


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_value(self):
        price = self.product.price
        return self.quantity * price

    @staticmethod
    def get_total_value(self, order):
        order_objects = OrderItem.objects.all().get(order=order)
        final_sum = 0
        for product in order_objects:
            final_sum += product.price
        return final_sum

class ShipAddress(models.Model):
    city = models.CharField(max_length=60, blank=False)
    street = models.CharField(max_length=60, blank=False)
    number_local = models.CharField(max_length=6)
    region = models.CharField(max_length=30)
    country = models.CharField(max_length=40, blank=True, default="Poland")
    phone_number = models.IntegerField(blank=True, default="", validators=[MinValueValidator(100000000),
                                                                           MaxValueValidator(999999999)])
    user = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE)


class Complain(models.Model):
    complait = 'Complain'
    product_return = 'Return'
    ship_problem = 'Ship'
    manufacturing_defect = 'Defect'

    topics = (
        (complait, 'Reklamacja'),
        (product_return, 'Zwrot - 14 dni'),
        (ship_problem, 'Gdzie moja paczka?'),
        (manufacturing_defect, 'Wada fabryczna')
    )

    user = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, default=topics[0], choices=topics, blank=False)
    description = models.CharField(max_length=200, blank=True)
    date_created = models.DateField(auto_now_add=True)


class CardPayment(models.Model):
    card_number = models.IntegerField()
    safe_code = models.CharField(max_length=3)
    expired_year = models.IntegerField(blank=False, validators=[MinValueValidator(2023),
                                                                MaxValueValidator(2028)])
    expired_month = models.IntegerField(blank=False, validators=[MinValueValidator(1),
                                                                 MaxValueValidator(12)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False)
    credit_card = models.ForeignKey(CardPayment, models.CASCADE, blank=True)
    door_payment = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_amount(self):
        value = 0
        for item in OrderItem.objects.get(order=self.order):
            value = value + item.product.price * item.quantity
        self.amount = value

