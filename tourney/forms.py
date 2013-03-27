from django.forms import ModelForm
from tourney.models import Player


class RegisterForm(ModelForm):
    class Meta:
        model = Player
