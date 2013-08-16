from django.forms import ModelForm, RadioSelect, HiddenInput
from tourney.models import Tournament, Player, PreRegPlayer, Event, Match, Card
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


class PreRegisterForm(ModelForm):
    class Meta:
        model = PreRegPlayer
        fields = ('first_name', 'last_name', 'credit', 'gender', 'phone', 'email',
                  'zipcode')


class ProfileForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone', 'email',
                  'zipcode')


class EntryForm(ModelForm):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name', 'gender', 'phone')


class MatchForm(ModelForm):
    class Meta:
        model = Match


class CardForm(ModelForm):
    class Meta:
        model = Card
