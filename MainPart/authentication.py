from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from MainPart.models import CustomUser


class EmailBackend(BaseBackend):
    model = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
            Our fuction those we use to authenticate our custom User,
            if we trying to login function is invoked and
        '''
        try:
            user = self.model.objects.get(email=username)
            print(user.password)
            print(password)
            if user.password == password:
                print('data')
                return user
        except self.model.DoesNotExist:
            print("User not exist or another problem ")
            return None

    def get_user(self, user_id):
        try:
            return self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            return None