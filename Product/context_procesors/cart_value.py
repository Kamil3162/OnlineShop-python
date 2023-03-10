
from Product.models import Order
def cart_value(request):
    """
        We will get a current value of customer and his actual order,
        Using session value we can get a information about his nickname
        Next we will get a instace of user and compate this to order.

        After that we will get a order instace and all actual ordered
        items and we will callculate actual value of order
    """
    try:
        order = Order.objects.get(customer=request.user)
        items = order.orderitem_set.all()       # we get all product to this order

    except order.DoesNotExist:
        print("this order doesnt exists")
