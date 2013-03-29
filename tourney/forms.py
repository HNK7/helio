from django.forms import ModelForm
from tourney.models import Player


class RegisterForm(ModelForm):
    class Meta:
        model = Player


class ProfileForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone', 'email',
            'street_line1', 'city', 'state', 'zipcode')


class EntryForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone')
