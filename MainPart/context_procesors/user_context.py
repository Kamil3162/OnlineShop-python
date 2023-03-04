from MainPart.models import CustomUser

def user_context_name(request):
    """
        Add username to template context
    """
    user_name = None
    if request.user.is_authenticated:
        user_name = CustomUser.objects.get(email=request.user)
        return {
            'user_name': user_name.first_name
        }
    return {}


