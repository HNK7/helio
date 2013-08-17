from django import forms
from django.forms import ModelForm, RadioSelect, HiddenInput
from tourney.models import *
from django.utils.safestring import mark_safe


class HorizontalRadioRenderer(RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ('title', 'start_at', 'end_at')


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('tournament', 'title', 'start_at', 'division', 'format', 'draw', 'game')
        widgets = {'tournament': HiddenInput(), 'format': RadioSelect(renderer=HorizontalRadioRenderer),
                   'draw': RadioSelect(renderer=HorizontalRadioRenderer),
                   'game': RadioSelect(renderer=HorizontalRadioRenderer), }


class RegisterForm(ModelForm):
    entry_mpr = forms.DecimalField(label='MPR', decimal_places=2)
    entry_ppd = forms.DecimalField(label='PPD', decimal_places=2)
    class Meta:
        model = Player
        fields = ('user_id', 'first_name', 'last_name', 'gender', 'phone', 'email', 'zipcode')
        widgets = {
            'user_id': HiddenInput()
        }


class PreRegisterForm(ModelForm):
    class Meta:
        model = PreRegPlayer
        fields = ('first_name', 'last_name', 'credit', 'gender', 'phone', 'email',
                  'zipcode')

# class ProfileForm(RegisterForm):
    # class Meta:
    #     model = Player
    #     fields = ('first_name', 'last_name', 'gender', 'phone', 'email',
    #               'zipcode')


class EntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['mpr_event'].label = 'LIVE MPR'
        self.fields['ppd_event'].label = 'LIVE PPD'


    class Meta:
        model = Entry
        fields = ('mpr_event', 'ppd_event')


class MatchForm(ModelForm):
    class Meta:
        model = Match


class CardForm(ModelForm):
    class Meta:
        model = Card
