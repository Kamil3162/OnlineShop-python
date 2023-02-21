from django import template


register = template.Library()       # to activate in template we use load

@register.filter
def dictionary_value(value, arg):
    """
        Function to generate average rate to particular product
    """
    return value.get(arg)



