from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.views import View
from .models import (Product,
                     Category,
                     OrderItem,
                     Order,
                     Rate,
                     Complain)
from MainPart.models import CustomUser

from .forms import (RateForm,
                    ShipForm,
                    ComplainForm)
from django.core import exceptions
def generate_opinions(query:Rate):
    final_opinion = 0
    counter = 0
    for opinion in query:
        final_opinion += opinion.rate
        counter += 1
    return final_opinion/counter

def all_products(request):
    """
        This function is responsible for generating all product on site
        Also generate average rate for ceratin product close view btn
    """
    prod = Product.objects.all()
    op = Rate.objects.all()

    def generate_average_rate(product: Product):
        average_mark = 0
        rates = Rate.objects.filter(product=product)
        for rate in rates:
            average_mark += rate.rate
        return average_mark/len(rates)

    def generate_all_marks():
        generated_marks = {}
        for product in prod:
            result = generate_average_rate(product)
            key = str(product.name)
            generated_marks[key] = result
        return generated_marks

    opinions = ""       #[generate_opinions(x) for x in prod]
    marks = generate_all_marks()

    try:
        username = request.session.__getitem__('username')
    except KeyError:
        print("Key is null")
    return render(request, 'product/all_products.html', {'data': prod,
                                                         'opinion': marks,
                                                         'opinions': opinions})
class Product_details(View):
    def get(self, request, id):
        """
        This part is used to display a particular product with
        all details and generate all comments to following product
        and generate empty form to add a opinion
        If user is active we can add a rate , if not we cant do this.
        """
        product = Product.objects.all().get(id=id)
        opinions = Rate.objects.filter(product=product)
        if request.user.is_authenticated:
            context = {
                'product': product,
                'opinion_form': RateForm(),
                'opinions': opinions
            }
            return render(request, 'product/certain_product.html', context)
        else:
            context = {
                'product': product,
                'opinions':opinions
            }
            return render(request, 'product/certain_product.html', context)

    def post(self, request, id):
        """
        This part is responsible for add a rate to particular product,
        First we have to get object product and user to get comment to
        product if this comment exists we return only view .

        On the other hand if we havent any comment from user to product
        we can add this comment to this product
        """
        if request.user.is_authenticated:
            product = Product.objects.get(id=id)
            user = CustomUser.objects.get(email=request.session.get('username'))
            rate_existance = Rate.objects.filter(user=user, product=product).__len__()
            if rate_existance:
                request.session['rate_active'] = False
                return redirect('all_products')
            else:
                opinion_form = RateForm(request.POST)
                if opinion_form.is_valid():
                    print(request.session.get('username'))
                    opinion = opinion_form.save(commit=False)
                    opinion.product = product
                    opinion.user = user
                    opinion.save()
                    return redirect('all_products')
        else:
            return redirect('product_view')

def calculate_sum(items: OrderItem):
    value = 0
    for item in items:
        value += item.product.price * item.quantity
    return value

def cart_elements(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            '''
                This part is responsible for search product using PK in ordersItem
                Next we are displaying these items using for loop 
            '''
            order = get_object_or_404(Order, customer=customer, complete=False)
            if order.complete is False:
                allow = True
                items = order.orderitem_set.all()
                context = {
                    'items': items,
                    'sum': calculate_sum(items),
                    'finalize': True
                }
            else:
                context = {
                    'items': [],
                    'sum': 0,
                    'finalize': False
                }
        except ValueError:
            print("Value error")
            return redirect('information')
        except ObjectDoesNotExist:
            print("object dopest not exist")
            return redirect('information')
        return render(request, 'product/cart_elements.html', context)
    else:
        context = {
            'items': [],
            'sum': 0,
            'finalize': False
        }
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
            ordered_items = OrderItem.objects.get(product=product,
                                                  order=current_order.id)
            if ordered_items.quantity < 99:
                ordered_items.quantity += 1
                ordered_items.save()
        except ValueError:
            raise ValueError
    return redirect('cart')

def cart_count_minus(request, id_prod):
    print("This is change quantity")
    print(id_prod)
    if request.user.is_authenticated:
        user = request.user
        try:
            product = Product.objects.get(id=id_prod)
            current_order = Order.objects.get(customer=user,
                                              complete=False)
            ordered_items = OrderItem.objects.get(product=product,
                                                  order=current_order.id)
            if ordered_items.quantity > 0:
                ordered_items.quantity -= 1
                ordered_items.save()
        except ValueError:
            raise ValueError
    return redirect('cart')


def finalize_order(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user_object = CustomUser.objects.get(email=request.session.get('username'))
            order = Order.objects.get(customer=user_object)
            delivery_form = ShipForm(request.POST)

            if delivery_form.is_valid():
                """
                    Each field have a data what we want
                    Problem is according to save this in mysql 
                """
                print("validating is correct")
                print(delivery_form.cleaned_data['region'])
                form = delivery_form.save(commit=False)
                form.user = request.user
                form.order = order
                form.save()
                order.complete = True
                order.save()
                return redirect('order_finish_panel')
            else:
                return redirect('information')
        else:
            return redirect('cart')
    else:
        delivery_form = ShipForm()
        user_object = CustomUser.objects.get(email=request.session.get('username'))
        order = Order.objects.get(customer=user_object, complete=False)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'items': order_items,
            'value': calculate_sum(order_items),
            'form': delivery_form
        }
    return render(request, 'FinalOrder.html', context)

def finalize_success(request):
    return render(request, 'product/success_information.html')

def category_products(request, nazwa):
    category = Category.objects.get(name=nazwa)
    products = Product.objects.filter(category=category)
    context = {
        'products':products,
    }
    return render(request, 'Category.html', context)

class ReplyComplains(View):
    def get(self, request):
        print("this is get request")
        context = {
            'complain': ComplainForm()
        }
        return render(request, 'product/complain.html', context)

    def post(self, request):
        complain_from = ComplainForm(request.POST)
        if complain_from.is_valid():
            data = complain_from.cleaned_data
            user = get_object_or_404(CustomUser, email=data.get('user'))
            product = get_object_or_404(Product, name=data.get('product'))
            order = get_object_or_404(Order, customer=user, id=data.get('order'))
            subject = data.get('subject')
            description = data.get('description')
            try:
                complain = Complain.objects.get(user=user,
                                                product=product,
                                                order=order,
                                                subject=subject,
                                                description=description)
                return redirect('product_complain')
            except exceptions.FieldError:
                print("This data to field is bad")
            except exceptions.MultipleObjectsReturned:
                print("You pass multiple complain")
            except exceptions.FieldDoesNotExist:
                print("Field Does not exists")
            except complain.DoesNotExist:
                complain = Complain.objects.create(user=user,
                                                   product=product,
                                                   order=order,
                                                   subject=subject,
                                                   description=description)
                print("Now we create a complain")
                return redirect('information')
        print("This is validation of form - not working  ")
        return redirect('product_complain')


# short hints to working with cbv
'''
    First try to generate dta usigng ListView or redirect View
    We will base on CBV - class based view using class not finctions
    https://docs.djangoproject.com/en/4.1/ref/class-based-views/ - doc 
    https://ccbv.co.uk/projects/Django/4.1/django.views.generic.list/MultipleObjectMixin/
    https://viewer.diagrams.net/?highlight=0000ff&nav=1&title=ListView_10Oct20.drawio#R7V1ps6M2uv41rnO6q0yx2uZjeklmqpK5neVmbj65sK1zTNoGD%2BCzzK%2B%2FkpAwAmEwSFjYdCXdNgah5dWjd38n1uf920%2BRd9j%2BEm7AbmLqm7eJ9WVimo5uWfAfdOU9vWIsDDO98hz5G3LtdOF3%2F7%2BAXNTJ1aO%2FATFzYxKGu8Q%2FsBfXYRCAdcJc86IofGVvewp37FsP3jMoXfh97e3KV%2F%2Ftb5JtenXh6Kfr%2FwD%2B85a%2B2dDJL3uP3kwuxFtvE77mLllfJ9bnKAyT9NP%2B7TPYodmj85I%2B92PFr1nHIhAkTR74ZgRrff%2Ff%2BfFP53%2FNffT19fdffpuSVl683ZEMmHQ2eaczADZwQsjXMEq24XMYeLuvp6ufovAYbAB6jQ6%2Fne75OQwP8KIBL%2F4NkuSdrK53TEJ4aZvsd%2BRX8OYn%2F4ce1xzy7a%2FcL1%2FeSMv4yzv9EiTRe%2B4h9PWv%2FG%2Bnx%2FA3%2Blx52sgcxOExWoMzc0VIOfGiZ5CcuW%2Be3ofmLfcCsig%2FgXAPYH%2FgDRHYeYn%2FwhKaR%2Bj1Obsve%2FRb6MMumzrZXJbjaLqzWMAPpmsbpkHeS3eaq7Mtpv0mjZzo5Ico8t5ztx3QDXH1a6eG7bAvmjF0Bz%2BkTdJvuTGfLmHavIBOTQ6dznZwFT49hbh3J4Kd%2FecY0h%2BmMSa5H%2BANhn14O%2F0IPz2jf%2BGMPEbgP0cQw0Zg1%2FSPcJZi8vHj91f07QN9Fex5%2Brb0We5O%2BdlbQQhkqNvb%2Bc8B%2FLyGFAcieOEFRIkPIeYH8sPe32zSjQRgf70Vbg%2FRKlkL2LjzaeJ84VLv2W0NXwTeeDhJXsJAEUOc5CkdktgsfbIjuU4htTJ%2FDJaKNFt3c39mM%2FYF4dNTDJICoQkhLauStA4R4FLWwdts%2FOA5pauF5iDCSqFFx0T35O393Xv6M3zK2x%2Fwj5Zlw3%2F3INiFpav4zs%2Fc%2ByGSri95AK5wHO7gvF3yyDHyIWmaegBeq5%2BDXQnjg7cG7HBze8zUdDM%2FHasw2oBoGnkb%2Fxin9%2Bj4Zzv3t557YA83nB9ME3Rw%2FMD%2FbRUmSbhPf3ZzP%2B%2F8AEy35CzGvVnkfn2FPZmuIuB9T3%2FEH6ceJo%2F0jhDulqdd%2BDp9haxM%2Fib0aBk5KJHACQnQvoIzHjNU8j3%2FTBU%2Bveb6O0esQ%2FE1f%2Fp4RfCrVhG9ugFPOVBKu0C7pdf2LHgqv2fjw9uT9bay2Zo2D%2BUmH9u2teI0FoNd9ZAv7xsm6PYTWG4wO0QU6WJYbvBj285xhpuekgqPVeRgUzZA4HA%2F4A1%2FtrnTXsczwP2vFwDyOyGN8I3CWWtN4FJDZmIbbhTtHDyc0CEtDqA%2FVDbWYNO9iiGvoEMfRB8UktdvmySHZUphy8DbA6EI2gei8MbkBVB2qabKVuid%2Ft4adFblFqGc5yWJ0M3Ttq075G5G0BYL2l1Wd8iYGSZLKLHBCW292FxmrB1u9sJ9gV0MxlNCxilxF%2FvgqrQbgeQYdWHvWhBSj%2Bf4qAQYlQAyzx14GSugK4wNJ6MbsjG8bv0E%2FI51s9aXVIGZN0GgDUusb4YJvz%2BTDiLVZ5xE4ffMuInuziyV6GdqvdiBp1M%2FOOazkq2h0qYwtYnFiOr%2Bp5nR9PVkYp1Z5No2b16ldlee3YExDFxqBaD25usYPulnbMDUTGoFrbN8TvJ2T%2FKYFNPnvKHp0xVt%2Buy2pjzrtgirIeITNDgTSwj30XsMksch2gh1UUbCKaQ9w2CtwtQE2dFqSL1FslYtzenLMGheFRL0VpBgKAcJhlqYYErHBMyZL8H%2BkLwPERZMsbAwt9kNLMiZwJgVmu0RFhx1YGGwqGAt1EKFmWxUOHjPfuAlYLl6f8QXw9XfcC8td36cDBElHFEoAcnRLLAOlhCMsFh%2FOKsvfLAUYhvmTQFC0wsYYRg1GIG%2FfQORD%2BcLEV1fwGGJBo6qEyZzoCQE5CxsthFRDpXOnH2RbS%2Fy7dU%2FMLecAiFL8MC0pDNOEDggliTLjZd4Q%2BScLGGck67pc9sVxCkVdC2OplscN0z5uGhQcVx93%2FK8uszuR0rSTaUYIoMK3rntjjcqnIINiJZJuIT75hAGMXgk%2B%2FbDNbZm%2FUqdp0Uh%2FIs%2Bs3isRtudK38rziuhfHR5Hl2ea12eRyKpI5KRCEYiuAcikOxB8MmLwc9%2BnBSDIH6kN4iPg0BsmgLOBXfoJDh6Pwgeq%2BLeD61d0W7LsSunBxa7%2Funvd%2BIelzfGi8RvSc6hPDg5mQ1HOuhEB01mUh1SUCBKS1AoTxB2QbCWW0JRH%2Bi10WRKyWU0o37i7fw1p7dIm6T%2FewvQe4gR0Q%2FRFx8exzoIkJ4Kcui6F6C%2FmdMkvcWD%2F5%2BgsZrJUHXsfvKAhrECSYKlsARCiL4JycjWWwAFFjJC9OsW9wrftAu9Db6EZLJjQE2wm8FNwWn5dBQvp%2B%2FBPoze63DzNkJIB3gA5Wz9Ig%2Bgtm0NbAabMMQiva17Ox%2F9avlpIGc0j5L%2BFQbVEUq9jQuffu15j1W5xa0X32rE6CA3cDf9SGyUW3wAb7CL8YNQlBHCXHaTJP1YPTFSWfi67X0kuYfpBhIJkW2F7N55WiUDc0fcGHHjEtxQZjeJTjJUS8oD2KGCgrA9%2FwxQtZrcfyTJwdZtkbAvkPqXKvSLy25%2BTSlSJ8q5VGE3%2BWpOFvrErdPLVb%2FK59Cq6TziO3GaoQ%2BtT2jeMLS8VpZ0Hj6S6hp%2F9OCxqInlqMWeRijWoHWDPFiYf6oZ7aWwcAFEcMnstPAi1%2BEc%2FA37BH3Zc0Bkmc5iazCR30G0wO37d6GALeWA4%2B6mL%2F1ZXInfsmCAuTdraz5qQyA1qm1u7ZzaZmALXfb6F7nUAjtat6dFMiDZ5UM%2BTcslVwvxEheldCnkZdmhOItP3vr7M27lc7gLUVBegLTz9Ffsj1r4xYvWJH5ilnWpW3YXxzK1QoUAGq%2BWS%2B8yn5N78uldLHqj8HiWRefgNVvnBa9laEQvFN1VYW9XHDI4G9KGKZhZ7DRHT2HpnvzdrriajUNreNTFxloxWYDyCYPW4d5fk8%2FnyU4EORkLnQ1gy%2BIyc9Rk62ViMmXRkmFdM46NTRXUNMC3kCpIXgIAt2nAm%2FB4t1bBt4Zus%2BTlELKRGktr2LJjaTHU%2B8HzEONo6f4SEZtnLEgwdRZcLSiq1tUK9XYKweES42jnQwmjzZVocl2XRSDLNmswSHCCgabAJLx6U7ezpjvjwkcKjrP0UOCBRq8KgAfb7Bhl%2F859QN7md8fIXXUid1HNnJ1H5m61C9ffs5%2FScL18I%2BnfPcbs5UedV2jYun7qAnaqnaJ5ymgkCKO9d3oLEkamPjw8gqQclYh%2FTCIviJ%2FgU%2FT5ALCjYJo%2FK0ZJVtv8ckSFI3fgf7CF9Bf%2F7VR9Qn5YoZT4lLZt9RBfKC%2FCK940oYZG3tW5K7xPTTvfX4dP0%2FQb0UES%2F3ZiVQyf8ONgH%2BO9jx3mt9g29%2BKD1zqd4LXH9AceCtWukmMOoukRj22FPuPuwAFG%2BJSnZtQ9lvpyNwRx4gUY%2FMM6or72oCcz%2FVcEDb9DaECZkVMf%2F9etj6qx6WsvBryb4gNY%2B0%2BobTjsrffi47V%2B9fEBgSeCxIaovubCNuGwvFYGZgGoPbwaWMtGN%2FrqpT%2FrRn8tb6XrkAlvNHdkVG3IJt6I796Kt8FPp%2Ff1OeX2KyTK%2BaLVRsyYBSUY%2BtsGGAkkIhljsBrhTnw1wO6e%2BLR9uAHVazsyaSOTpiaG3tQ2u27flhvw5B13yXLvBd5z%2B2Jp4xkk8AxSMFqsl5FLiD%2F55%2F4QhQcQ7d4%2Fh8GT%2F3yMhNYDrZMUBPO4sclZ36bqr%2BpWK6NC4g7hINyuppEfez%2BOkY0nzcpCpQ%2BIF%2FoX8OSnFqGuSr37nGGNnDWfc2NVt7NMpiEd66TDFxBF%2FmYkgfazytaa0xp0vR0Ldw%2FRUUITPoxhUYp1sFFYVC%2BBTAL60EZHJ4UL5nBh1MNUMALdkxCZd9QViElqi0KiQ%2F0lTOCAxKv7M77IWO9uxhfOLMZCE4cpYXhREe8HSWo9pDjijEVFnW%2Bbbl73xMYUoUhaT8nlDSQQv9J8SeeQ7vbUPJEXFnwK73WypjvFY9qFcEyD1J7MR2M6M70cjunQQoTiY2SuW5C5TUCUoem6PWECohZuXVCm4IAoGoFZGxElvIB7u0hNe85GlTuu0UOkptTC0ByMHUoQlsD6z4a7cJmVnZpigjQtW1uwlRnhZjXd%2FJ%2F%2BojbNMXJLncitsdJa4TXXjYySoQRr29YYGUX%2BPV0pfSqEHj35YLeZEGsf%2FoIswrgExxEHr6RxSKdVJs9R9lg7%2F7ablhoGprJuuFMlSjQCZBjDLBRFtzkJihyLI8QYuiwhxjQHJ8ToGqoez2Z1MHvO6mAMM60DLREuR6zg180aiGRBN4IQyWJms0lanGFlezDGdA%2Bj0DBYoUGmxCCpxuMoNIzpFFB4%2FUz%2FI4KIiz%2Bh558ymeUF53bU4214xDIPzQEDWYtcendcdzHN747bwHnRaXNKTwMeKnLhxRn%2BT%2BPEGQWwMzf6hnwEgDemFhjlyjZtceTK5niutmg5NUwqSxJmkSda8tKVGvSieGHjOgkDqZg45ciJjjuftJATT%2BKqvTAn%2BTyorjubnBVa4RdxUqe1uJbUWWHpmBessiVjazok8ph4QcWUlaYQy7P8eqpDkWdFpivUXTab6dQQItBOkWGsL6HWNrir1Zumy14UkGNxHjnOqLtMq5W6SywY0cyztWBkWVLQ6FJDPiQ2h0WrGdGq%2FliZbdeZd31i7s4KxCzBW8CuNvLeOwzaVazUxTAI%2BQnTsFiPAUFZnU1Xo%2BrHvrM60zeNqr5R1Tc8VZ9k%2FwA%2B8t2ytk94PigJOatGjaRc7dVPaLWI2jE47lcYGZn8rtjFgm4OBBTvubDrVN2IU9ZQPWbqhxHknvLDYFTijUq8Fm1xMKY5TCuuxDMtwy7UsLKpRiWvx6NyTD96PGt4fu65SkN%2FMfKx6LJDVLatF4Jt0UJwtzWV5l9%2BPIDo8YNWLNH4%2BPEj%2BTrAykCWMK9zJEQuCm7nHZ1D5MuIVOi9DgCc9PiZ7sxw5s1wAMW7zBgk0CzTrUGDHnRnjWHDFA4b7XRnhk09EKley3FrNGHFJ2ynD02YLlMTVpAJH6lwM0RIoy5eQiBNp9aGzvXNDLjbZwzdTM1ZX8ow274qp8NgnNm0wqLmuiYLcWbfIX2N4cxWxBRgWA7LZi%2FsOsX%2B3NQ7PjHX%2BwBAyqpIA0DK1YVYJYcTHw0ZCOmeF%2BL3O6d20s44WBADp25vdlLnqiCIuT2XQUJ7bjaDQsjtGQVuz9BrLaUcxu5q8LgQDY%2BdhERHKpZkjFSWYJDN4Qh%2FB0vU0gBBxREGKnA%2FGNaMNQ6KilM2LDZKGb5rrjNhyr1FHFjVgSmjGXI0QypuhpRpg8wr0QQa0W7XCCkyP1EfFlLCR6d1FIXZV9Lfha2w6AoUwldYZAqq768Q41onUr5Fi3XeJEwAaVJR5rN3m2kbp4NWNHZuS0nb%2BX3ZjIWnRxUytrEqUFtM7otuzlYYuTlPg%2BZntTgwy%2BRgldBsYOumoDNfX75yfZEpRy08Emwngr1kRkfC7dPBTjSzVA%2FxLUSsKxX5IzCLRANFxMWKCVe5f0Oo9OvH2ZG6GZG%2BNXaWzCD3g%2FFStrVoHL1O2vxMyaLOvuItoPAyW3XqLl5prezEUafAlgLnYq%2FzDxCTqvr093Xi9zfz%2BSNY6dlvxCsMdRVySiGlF6HhCS6nQFz7wnTXV2MOR%2Fga2YZBsw1XtrzeM8twN1OvJs%2FAm%2F40eeGtzf%2FILQyfWxCt%2FxVsOxmN5v1huqKMXouROHVMmSyKbtPXLhypQvUkhZtf206yZCX38bDBmUKEUYBIzbYEdz%2BFz67u9SZX5UZx1L%2FI5a2bwmsRsooe2bLdYcWfNXWrOxGZpiXKVyKVkXm5GEs6W6BIwEkxa8vM1SelrC2OtMI%2BhmFdNZj5grQtCLhIg4Z9blXqI%2B3kpEsoh07RSrM0tLeY9zgN9SvlPb48UFkvlIwybFIfqjLu2J53fWK2qHlgdvb%2BiZyKqEY5UyU9ufuPA6wn2fObUkhgoO3O2DJDU0H5SC2rGH7cWz5Sq7zK9FQ4jIGAzHNjIGCOpeiJe%2F6c8kJ9JyJVjeUcZBDgnYaICe%2B9ZBELHixwE3nHnRKecFwdPop1E6q870TrvRQBU1ij0UkbPzBvUXgIRN5SgJl%2FtBHcvI1AaZRXRyN8kwhwYxDfXWndcnvI0UTaEzmaSKOo%2BjHnXFWkZXJUkRITSFdX6Rpl%2BlGmv7ZMP9YYGZJkz0HyscYI91PTzvfX4dM0jTVGKLWIWcPhcWQDY7tvpsaIYVksk5gxg9erMGLPhmKqbm%2BalpT6mpvbmk2gvnAL6ybKOA2hYc59k9wM17SwrZSstGccF094i4%2BanCO3tg83YKct4dC89DN%2BkMkTVHg6r2Mqn0KTwWS6pVtXiEHbMgXlzzZ0S9OdfCbbvuzX9pjIdpR1Byvr9mHDViyd0RAFXgEpY29R5mWESkxeqUiZXkGCJZUrV%2BjCMUbB6DraAWxqU224Ytk92UIlx5j0YbUbZfF%2BFv7KuQW6xQuuyk1uvdhLEqERFwLXR87x1O0U5frxYFFNpCNPhyN0eKjBndK2kxn7vBV3Wrsv8DpXE3TdwGOF28cue1vK5pEMv3jXKNo3rIJRtG8nxZDap9XwMuEoAogtfckUNxhwipLPqHkgZzKw5w7HZFBUPYurTWaUJqrvKnXWhKlJbE%2BaFambMAXqait1Cq07TAvM1Vaiowss3Vph6QuT9VkyUPjk7KS5LVR%2FTcdYMl5wrBOoLirrDVU0YAkzhJiLguOVPjdreld%2BhFQZl2o8cUyZxhPGnyWMDlsviB%2BHWL6vCiUvNmqgID2WCqeGEAuHbWqWkbNvLFibnzmDAJX%2FM%2B%2FLAOLMrwnMbA1lS28HyqaiqGy7vaHyfKEtCugJ2QB7kaO4RrjcAksLdeMNg5ToPYOlxUfMupBns%2BgF0eYRx7R6QOxq51mxiB1GVQVYqeMVxnP4IrZ8K72Ob%2FJ2u%2FB1CfaH5H355Ecxbh3QZ3K%2FDvFUoI4HIkzd5qxQ5t4UcixMLXgwLNwc8NvsW%2FTCtpV4ELhXPQgucOrJjgF9chFv3gPiW3K8hi7PQ7FwiuBn1%2BClYRU53MsfcVlQloOwNJuFcIR9zOV8p4B6%2BqQxmr7s6taLl2GyBRFGTsg%2BDxEpXZFIaSwKZaoFQaVhzLRiAg2zL3SkJb2vhY66bjKssjl3mmHkQFjlmXFFVtkwHE13TmdwgaqEscqZ6272YsuoY2KLj5h6D2qHWbVXnCAmNsdaDlHjQOFAhMbBtFxmicUkBXI018o7VLIkr2uLWf7XeW8Jg%2Bxq%2BWh0uBwdLhV3uJQYXKhkYbEhelveb%2BWzgfuDfjtFD6b%2Bnax%2BC3llQcAEkKO%2BisdndZTZmSJh7ZxU8O934h3IqDR7xDw5SVzuFXzE%2B8xTNbUwoj23q252S%2BX0%2FeJ21gcxpVkuH1iFuWKkkXY0kptOoeTRXxV7DGU4M1AH9Ln3E7jBJMpYt3HFWq%2BY0qnintUQXbsQ%2BmViVwc6FpNSsZP8MTDSjwBksZX1tf%2Fp6x%2BK9mzclYPalXtOfI1RMz9XjUPAxghx4uSVcrBiWqQJrtRhT3gxhdjao%2ByG7mUrK0D24G0NDl0SGuNwk%2B79%2BBOZ075GkVAV2oCCgUSX%2BJQjoHQCAW78Jryrt7q0zZf8NkGY29NuemvJTB%2BcxNQtbSjbWMloxt5nIfL8M9PQilL%2FkSQHGzkXK8kxLFXoFxdfv%2BFzQEeFE3RcuUCffDUnC33ifkbQS798SU2UAc4Vt8Yv8NHNK5KmBvsJbSYknU36e5BoQnMZKM0n3Y54MB5JKgkHwhURNXxHf%2BJL%2F6dO13h6%2Bcsj3ElAim39VvsnGRlUTEM0rBksxKKIhFm1uYvuWphym%2F8MXrydv%2FnW7cgXMz6vS90uztjUk7FGuSrbagIBQV25iuyuCY2y09s3z89E9pjj5j4ITUv2IYs0ENrfPYhj2GWxfRWbLE%2Bs5NMpExsPiOafakYrWNnDnfAc2fWll5WmZBXLbfW3BmQrKTT%2Fq3KLsbL5QFUw3l1AAlwo%2BFL34om8LG5s4cDK4NlLcrqVKgXqBrmQS%2Bk2o%2Fmy8indbGlVYGbDSxhxygOXyxphzyY1IdHoWzEmGnGcpJPG2WWuj5F2G8ZI09DJPpK8GZqVq8fBRt0bpm1p7qwUWyo8TdvMKLx4ThIHnUktVMx70eIRekFqiDXd0Lk42HyenjBaYqQr5vghsn0xxU8%2BqU8ZWEmAabCKD5NKJ3q42egPu4J7PXrXx4%2Bp0%2BmHa0Rl12%2B2swglptiN7bJZNS0hcdqwk9rC5jXcQyy2W6JBSj6HMRabeW6MxWa4%2FF7UNUoUeu01JrGyrTEOW5IyPztP1e2jUpGQPL%2Fk1qqwXhQIF8uTnCUYWtzhH9FRHZLmDPfjx7a94yxOt2Aors5i4IkUfiOWfB13ww%2FixAvWhfJaueON1GJOttjL6cUHr9r59uVMjiJeDAOLhyrIiwK3wZhAYeQaBJ1R4vsnjXW4LeZAendHbkEJQ8Mia7qjoWFBMxtSZag9dzSqhs2Xj6GVYvopHzO7bpWCC2wN4uwCvdV0MWdmQQNuW4WFFKfSnxVeZdTm8XeLealbPGLN6x4pzUHhETlWALrGowZ21MCOGtjcm2WnsGrbVg%2BK2MGrHy7ofH8dPk1Tph1JFSF7783fH1GpceoNlapJMqLTwVsCgk32AI77yvwWV%2Bj8e92CapWDGqMmmwmeHHXah2v3VBhxjbqnfnRPTQFaoiQkRPZxCyygS3nVnNzj0HsYuYeyccLlnvlVy2ZeR%2B7prRSEaRW96iTKPcVXWayTUZPeWb34JZkliaRYC4xLkmp6AM2rYOBiDyBdM1yT1Y10LQ3ZQ9Uao7SYo3g5ipcDES9lypaSUt%2BOYuUoVk5m6D%2FsgoE%2FTUjpglR6ROZ19M5teNwhmXLjx4cdZiYIMeooABqJnR6WOdM2fvRQYhzSnNLTgIfqIfxDUZGnceJMKDgAE31DPgnA24yi6CiKtmjrvFVz6FIoDdjJzB1UDsiLobxQH0NeqE%2B5aFdFUWEVJQNhMsDUdFwUQQSXZGbPdWexKMSnWAtXQwExtmmZrmsuzItlUnuuGYWn5IkHBq3Drb56ob06waDlHKXrEwybDRAx7FlhQ4pSJ5TfVKdNqHtCjjLB0KsFUAGFJCE4HKBACEio1ADrSGY7UEiIkrEwnG4qiXfuAxIRyLiqY4eRw58TGrUIIjUWk6vGkGYgVxtEahgz0XDYibUwjAreAknpCQpGRPxF4O0B3uAq8hfnKVuI6tFcCIo2NFjmEpWfdftjN8q65VEdOaojVVFH%2FkHQ5jfCVvSmkIRQApdumYRLytHciU5SuNc73JAQbNUJHpDtzZxxwGMQ1FDVxR4%2B1em2R9h%2FjNGJRxXGk5nOyjmpSrkUs5U%2B%2B%2Bon27RRpUdPGTs8dgR%2BWCtMOp%2BO%2BxlyOUHKLKEtrbqq%2BBsOvtJLGzLN%2BJ0OCbELSXRcp1F3uWC80%2Fqn3VV9sMJ23gWwIQ%2F9JKumITcNWQbvuFOiXg83YRreYwGUt94PYrOmdTo8B2aCyE%2Bi0IN4NDMps8aFk7i%2F%2FSwndFF8McX0dyXkDbULUV6IljKp4MSMjWRw8eSV1ZQiUeFqldY7CtLSo5j7FfRlzjSR9lSY54FtvWzbgeDZD%2FoKYRdGC2rphlqykS0Y1kEFxNv6XGMt5wteVAjPHceitl3xNjPzqn4brNXUbGg2zb7kHztjMRVoHKUmzwbGUVct46hZ9p%2BIjwcQPX4YvH2U0rAQzwdz4Xazj%2FZg%2FTTta27aVvmyDXbPzpXcs%2BL9uzruWae0Z4lcMKDNaYtzXrAM12WdDrpt1UL0VR9OSrPRb2H0W5i09ltY0QtswFOtv0FFfo0Vw6m38DeQq7NQRfocjdo9dbjCqJ0WciRmzpO9l9BbahfFUUHHNCaIWrRTgyhWrmrw4y9H3EyNpUGN8dNh435jl%2B60ZnRaBhoiSRr89DShZm%2FW5yctM41AJoJHPAhGM7Asu9VtlKM%2BD92tNFDntIcN%2BrjiQDiSV0WeL3X6pZu1BKi7naTUX90fohCSzu79cxg8%2Bc9H7CM0rD27NppMbyPUteCv%2F8wfpZjE8JkRPOBAmgNY%2B08%2BmqTPuKWHODt%2F0LkEZxOKbCjP1XQ6uJG%2FopH%2BnXICceJF6F%2Fq6oY6kI%2BdvuTUvGEs5tF8qhaQAiRSSD3Nt5bykZg3QoTMVsR6BQ%2BpBB%2B8gIDSeoHdRByYlzKZYUDbHcAkeIfDhOYB2IcbsCPjQezlH6nnJxkePHvQt8MRz0CSzV2aty7nadjQ1q%2FG%2BMngCAHEqSMlHh0UGaIp5CwOOwx4mVBBeGeQjRcpRPceVp%2Ft3tviXr%2BjfgYBiOASpeQKLnIG7f3k9zvFQnDYxa0Xe4kapVEHZg4PsVJpme6WXkzhDdQi3PK8CMrEVqa%2BkgAWHhKlzvz7o1jJPSSnrpJ9W%2B5BckmcR1%2B87nVnBfJMmOm5%2FvERmzw0bagdq26VU4BtYjqtl4Pfyx%2FFd09sFzVsMK2fzXYgjEy4IgUvkdXZz545V997yx02aKvCfwxr%2FvBpQ%2FQ6ikzgwDgKRjm2jI9PT%2F6bwLn8oLYWdtdJGgtfhfQCaxxFbljRqvRehAVB4VUoX6LY2ZSsVhcRx3TBNPfKYz2ud%2FEHwYwWtnT7EVZeAT%2FZYg8bpMJ8YKDsAV1NkshfHbFWs%2FEYe53vkHYemcKomhZZrnQoqmxDpNAi%2BrvUmk81ur%2BiW38HWHM%2FDIZuMhc98ZcsAjeEdxcLjdw9A5LD5hpe9uXGlmk853KpbgcxQ9O6fxfyhVKwg7uN2lqjur1XaTauc0x1Sx5KZFxO0e%2B4Mk7Hzl7VKU7HKpQV5AXpzHlBOlk9Fwl%2B4Obw%2FP01Xc98%2FFOff8ueTa6b2pDG5AwvtaFplf3GnTR1KevF4XwZVHAATeMnInJHX9DUhmTr2t2iA2jL7kKjTdGAAcvuL2LAHSMGxoiBSW3EADui9HRE9wQhjmcuS1p9MCBXy4M4xiUIZ0nHuAT03xiX0CEuAStwxsiEnsC3kwpfZb1LnbWmw7AFWS78Lr48vKn%2FVyg2K8louLgTw0UFB6ZXGQsgK%2BYHfuJj72Z8sHUGOynjKhs1UpMBasuHvwAoxyRefhwPvDQXD41HdzNKQbATmhR8SFDSVR3KG77TmnBu8ohtM4N1mnuR6uRK9bFhZG130h8bNtUD09rftBJ0PssTLcSWVyCbIoqu7Z3127fpp9%2Ffwc%2Bvx19fX%2F7a%2FhpPy6l%2F6NQeuNuprKpA28nh4nG2QsVrpCrTk7dmG%2F%2BcKXP%2BBV6rm9z4L9y%2BoVx9U7KKqGt4Iev0Gy1LQ2UIdg7Sshko3VVNznhwpatspans1Q16vzjXe87Lsq7%2BQD0B4pqB8HtcuvP8fJ9VPNYp%2BfoglPQaUwFSx42mRVhbrusZhBz2RLF5qslMNRBV7nSm3pIliVMg4WjjhFVOGHww8paEwMapOjdV2yQ5LFO3KKrqJtMFmVMk9Tyk5pGHQxifPh9PH71kvaVfNmAHEkC%2FbYG3oZ%2FDA5KmYvoVLs8a3teEebuz9aDxtSPJVk4RNlKlpWnGWaqcpYP3TFLuZvP0gK7Veefd5Uyl1aNX7yNJNZqorMw2mS19nCr%2BVIURrdBBD1XaKfwE%2Fe1h87cXPIfaOoyAlj2qfaOfHrLHOomINzvbp1Qc4%2FatnqVi0ZhGJEkVd1mRa61oFBiJ8%2Fy0l8oDjDTaYLKkCrk8XZmYsbTUW%2FLjBSnbhjMT5Pk2Xv8vUwzuwvV31Ae%2BD2DqjEac1HL%2F23rJ%2FS3vJ0Z%2BYDwI9XPKRaQEzPWkfpG4qlPejSWFMqtk7mQEyLT%2BbtZWJ6W%2FOWd1%2FlPDLSv95wZP6b%2B4XOkPv0YhWo2Toykc4vYXLHdaX%2F8f
'''

# try with detailview and listview
'''

class DisplayProducts(ListView):
    model = Product
    template_name = 'product/all_prod1.html'
    paginate_by = 10

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def get_context_data(self, **kwargs):
        context = super(DisplayProducts, self).get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context


class DetailsProduct(DetailView):
    template_name = "product/detail_product.html"
    pk_url_kwarg = "id"
    model = Product

    def get_context_data(self, *args, **kwargs):
        print(kwargs)
        pk = kwargs.get('product_id')
        product_pk = Product.objects.get(name=kwargs['object'])
        context = super(DetailsProduct, self).get_context_data(**kwargs)
        if product_pk is not None:
            product = Product.objects.get(id=product_pk)
            context['product'] = product
            return context
'''

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