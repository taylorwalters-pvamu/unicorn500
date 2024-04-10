from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']