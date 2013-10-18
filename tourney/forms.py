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
        fields = ('tournament', 'category', 'title', 'start_at', 'division', 'format', 'draw', 'game')
        widgets = {'tournament': HiddenInput(),
                    'category': RadioSelect(renderer=HorizontalRadioRenderer),
                    'format': RadioSelect(renderer=HorizontalRadioRenderer),
                    'draw': RadioSelect(renderer=HorizontalRadioRenderer),
                    'game': RadioSelect(renderer=HorizontalRadioRenderer), }


class RegisterForm(ModelForm):
    entry_mpr = forms.DecimalField(label='MPR', decimal_places=2, min_value=0.1)
    entry_ppd = forms.DecimalField(label='PPD', decimal_places=2, min_value=0.1)
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


class EntryFormOld(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['mpr_event'].label = 'LIVE MPR'
        self.fields['ppd_event'].label = 'LIVE PPD'

    class Meta:
        model = Entry
        fields = ('mpr_event', 'ppd_event')

class EntryForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    gender = forms.ChoiceField(choices = (('M', 'Man'), ('F', 'Lady')))
    mobile = forms.CharField(max_length=40)
    entry_mpr = forms.DecimalField(label='Entry MPR', decimal_places=2, min_value=0.1)
    entry_ppd = forms.DecimalField(label='Entry PPD', decimal_places=2, min_value=0.1)
    balance_membership = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    balance_signup = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    balance_card = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    qualified = forms.BooleanField(required=False)



class MatchForm(ModelForm):
    class Meta:
        model = Match


class CardForm(ModelForm):
    class Meta:
        model = Card

class PxCardNumberField(forms.CharField):
    def clean(self, value):
        num_str = str(value)
        if len(num_str) != 16 or not num_str.isdigit:
            raise forms.ValidationError('Invalid Card Number')
        return value

class PxRFIDField(forms.CharField):
    def clean(self, value):
        num_str = str(value)
        if len(num_str) != 20 or not num_str.isdigit():
            raise forms.ValidationError('Invalid Card Number')
        return value

class CardScanForm(forms.Form):
    rfid = forms.CharField(max_length=20)

    def clean_rfid(self):
        _rfid = self.cleaned_data['rfid'].replace(' ', '')
        if not _rfid.isdigit() or not (len(_rfid) == 20 or len(_rfid) == 16):
            raise forms.ValidationError('Invalid RFID number format')
        return _rfid

class CardCopyForm(forms.Form):
    new_card = PxRFIDField(max_length=32)
    current_card = PxCardNumberField(max_length=32, widget=forms.HiddenInput)
    current_rfid = PxRFIDField(max_length=32, widget=forms.HiddenInput)


class QualifyForm(forms.Form):
    league_card = forms.CharField(max_length=16)
    pc22k = forms.CharField()
    subs = forms.CharField()

    def clean_league_card(self):
        card_no = self.cleaned_data['league_card']
        if not card_no.isdigit() or len(card_no) < 12:
            raise forms.ValidationError('Enter a valid league card number')
        return card_no

    def clean_pc22k(self):
        pc22k = self.cleaned_data['pc22k']
        if not pc22k.isdigit():
            raise forms.ValidationError('Enter a valid number of events played')
        return pc22k

    def clean_subs(self):
        subs = self.cleaned_data['subs']
        if not subs.isdigit():
            raise forms.ValidationError('Enter a valid number of league matches played as a sub player')
        return subs
