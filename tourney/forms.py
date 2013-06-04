from django.forms import ModelForm, RadioSelect, HiddenInput
from tourney.models import Tournament, Player, Event
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
    class Meta:
        model = Player
        fields = ('user_id', 'first_name', 'last_name', 'gender', 'phone', 'email', 'zipcode')
        widgets = {
            'user_id': HiddenInput()
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone', 'email',
                  'street_line1', 'city', 'state', 'zipcode')


class EntryForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone')
