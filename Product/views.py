from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View

from .models import Product, Category, OrderItem, Order
# Create your views here.

# method get is used to display our all view to product
# method post is used to add product to our bin


def all_products(request):
    prod = Product.objects.all()
    try:
        username = request.session.__getitem__('username')
    except KeyError:
        print("Key is null")
    return render(request, 'product/all_products.html', {'data':prod})

# 1 dispaly kazdego produktu na naszej stronie - cena , nazwa,
# 2 wchodzenie w szczegóły naszego produktu opis itp jedynie w opisie produktu jest dodawanie do koszyka


class Product_details(View):
    def get(self, request, id):
        product = Product.objects.all().get(id=id)
        return render(request, 'product/certain_product.html', {'product':product})

    def post(self, request):
        pass

# 3. wiew z koszykiem czyli display wszystkich prodkutków i sumowanie naszego zamówienia
'''
    I can do display order like based class view like get - display all
    Second get - display all componenets
    Thrid post - delete from 
'''


def cart_elements(request):

    def calculate_sum(items:OrderItem):
        value = 0
        for item in items:
            value += item.product.price * item.quantity
        return value

    if request.user.is_authenticated:
        customer = request.user
        try:
            '''
                This part is responsible for search product using PK in ordersItem
                Next we are displaying these items using for loop 
            '''
            order = get_object_or_404(Order, customer=customer)
            items = order.orderitem_set.all()
            calculate_sum(items)
            '''for item in items:
                print(item.product)'''
        except ValueError:
            print("Value error")
            return redirect('information')
        except ObjectDoesNotExist:
            print("object dopest not exist")
            return redirect('information')
    else:
        items = []

    context = {'items':items}
    context['sum'] = calculate_sum(items)

    return render(request, 'product/cart_elements.html', context)


def cart_add(request):
    if request.method == "POST":
        product_count = int(request.POST.get('product-count'))
        id_prod = request.POST.get('product_id')
        if request.user.is_authenticated:
            product = Product.objects.get(id=id_prod)
            print('This is add to cart')
            order = Order.objects.get_or_create(customer=request.user, complete=False)[0]
            order_proper = Order.objects.get(id=order.id,
                                             complete=False)
            print(type(order_proper))
            try:
                ordered_item = OrderItem.objects.get(product=product,
                                                     order=order_proper.id)
                if product_count > 0:
                    ordered_item.quantity += product_count
                    ordered_item.save()
            except ObjectDoesNotExist:
                if product_count > 1:
                    new_order = OrderItem.objects.create(product=product,
                                                         order=order,
                                                         quantity=product_count)
                else:
                    new_order = OrderItem.objects.create(product=product,
                                                         order=order,
                                                         quantity=1)
                new_order.save()
        return redirect('all_products')

    return redirect('all_products')


def del_from_cart(request, id_prod):
    if request.user.is_authenticated:
        user = request.user
        try:
            product = Product.objects.get(id=id_prod)
            current_order = Order.objects.get(customer=user, complete=False)
            current_orderer_items = OrderItem.objects.get(product=product,
                                                          order=current_order.id)
            current_orderer_items.delete()
            return redirect('cart')
        except current_order.DoesNotExist:
            print("Model nie istnieje")
            return redirect('information')
    else:
        print("Hello world")
        return redirect('information')

def cart_count_add(request, id_prod):
    if request.user.is_authenticated:
        user = request.user
        try:
            product = Product.objects.get(id=id_prod)
            current_order = Order.objects.get(customer=user,
                                              complete=False)
            ordered_items = OrderItem.objects.filter(product=product,
                                                     order=current_order.id)
            for item in ordered_items:
                item.quantity += 1
            print(ordered_items)
        except ValueError:
            raise ValueError

def cart_count_minus(request, id_prod):
    if request.method == "POST":
        print("This is post method")
        print(request.POST.get('minus'))
        if request.user.is_authenticated:
            user = request.user
            try:
                product = Product.objects.get(id=id_prod)
                current_order = Order.objects.get(customer=user,
                                                  complete=False)
                ordered_items = OrderItem.objects.get(product=product,
                                                      order=current_order.id)

                ordered_items.quantity -= 1
                print("success")
                current_order.save()
            except ValueError:
                raise ValueError
    return redirect('cart')

# 4. Określanie metody płatności

# 5. wpiswanie adresu dotyczacy doreczenia naszej przesyłki
''' 
    6. DOdawanie do koszyka i update ilości w koszyku !!!! - musi byc przycisk
    po buttonie musi byc utworzenie obiektu, 
    po kazdym odaniu jest zwiekszenie ilosci w koszyku  
    po utracie sesji koszyk moze byc czyszczony 
'''

# 7 podzielnie towarów na kategorie
'''
def divide_on_categories(request, category):
    categories = Category.objects.all()
    return render(request, )    '''