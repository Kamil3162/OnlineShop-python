from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model
from MainPart.models import CustomUser


class EmailBackend(BaseBackend):
    model = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username)
        print(password)
        print(request.POST)
        #email = request.POST.get('username')
        #print(request.POST.get('password'))
        #print(request.POST.get('username'))

        try:
            user = self.model.objects.get(email=username)
            print(user.password)
            print(password)
            #print(user.check_password(password))
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