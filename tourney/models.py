from django.conf import settings
from django.db import models, connections, transaction
from datetime import datetime, timedelta
from django.contrib.localflavor.us.models import USStateField
from decimal import Decimal


class Tournament(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateField()
    end_at = models.DateField()
    players = models.ManyToManyField('Player', through='Entry')

    def __unicode__(self):
        return self.title

    def is_over(self):
        return (datetime.now().date() > self.end_at)

    def total_entry(self):
        return len(self.players.all())

    def remaining_entry(self):
        return 500 - self.total_entry()


class Address(models.Model):
    street_line1 = models.CharField(max_length=100, blank=True, null=True)
    street_line2 = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=100, blank=True, null=True)
    # state = models.CharField(max_length=100, null=True)
    state = USStateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='US')

    class Meta:
        abstract = True


class Player(Address):
    gender_choices = (
        ('M', 'Man'),
        ('F', 'Lady'),
    )
    user_id = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=gender_choices)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=40)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.phone = ''.join(e for e in self.phone if e.isalnum())
        super(Player, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name.title(), self.last_name.title())

    @property
    def card_number(self):
        return Card.objects.get(player=self).cardno
        # return self.cardno

    @property
    def rfid(self):
        return Card.objects.get(player=self).rfid

    def is_profile_valid(self):
        return True if self.card_number and self.phone and self.email and self.gender else False

    def is_web_member(self):
        return True if self.user_id else False

    def casual_stat(self):
        cursor = connections['hi'].cursor()
        cursor.execute("SELECT ppd_ta2, mpr_ta2 FROM useravg where rfid = getorigrfid2(%s)", [self.rfid])
        r = cursor.fetchone()
        return {'PPD': r[0], 'MPR': r[1]} if r else {'PPD': None, 'MPR': None}

    def update_stat(self, mpr, ppd):
        cursor = connections['hi'].cursor()
        cursor.execute("UPDATE useravg SET mpr_ta2=%s, ppd_ta2=%s WHERE rfid = getorigrfid2(%s)", [mpr, ppd, self.rfid])
        # transaction.commit(using='hi')

    def stat_rank(self, tournament):
        entry = Entry.objects.get(tournament=tournament, player=self)
        ppd_rank = entry.ppd_event if entry.ppd_event else 60
        mpr_rank = entry.mpr_event if entry.mpr_event else 9
        return {'PPD': ppd_rank, 'MPR': mpr_rank}

    def event_stat(self):
        # try:
        #     event_stat = EventStat.objects.get(pk=self.user_id)
        # except:
        #     return {'PPD': None, 'MPR': None}
        try:
            lastest_entry = self.entry_set.latest('created_at')
            return {'PPD': lastest_entry.ppd_event, 'MPR': lastest_entry.mpr_event}
        except Entry.DoesNotExist:
            return {'PPD': None, 'MPR': None}

    def is_membership_valid(self):
        try:
            latest_entry = self.entry_set.latest('created_at')
            exp_date = latest_entry.created_at + timedelta(days=90)
            return True if datetime.now() <= exp_date else False
        except:
            return False

    def membership_expire_at(self):
        latest_entry = self.entry_set.latest('created_at')
        exp_date = latest_entry.created_at + timedelta(days=90)
        return exp_date

    def is_pre_registered(self):
        return PreRegPlayer.objects.filter(player_ptr=self).exists()
        # return hasattr(self, 'credit')

    def is_registered(self, tournament):
        return Entry.objects.filter(tournament=tournament, player=self).exists()

    def is_qualified(self, tournament):
        return Entry.objects.get(tournament=tournament, player=self).qualified

    def is_lady(self):
        return True if self.gender == 'F' else False

    def is_paid_for(self, event):
        return True if self.signuppayment_set.filter(event=event).exists() else False


class Entry(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    # casual stat is copied over as rank stat on registration
    mpr_rank = models.DecimalField(max_digits=3, decimal_places=2, default=9.0)
    ppd_rank = models.DecimalField(max_digits=5, decimal_places=2, default=60)
    # event stat
    mpr_event = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    ppd_event = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    balance_membership = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    balance_signup = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    balance_card = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    qualified = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)

    class Meta:
        unique_together = (('tournament', 'player'))

    def __unicode__(self):
        return "%s registered for %s" % (self.player.full_name, self.tournament.title)

    def save(self, *args, **kwargs):
        self.created_at = datetime.now() if not self.pk else self.created_at
        super(Entry, self).save(*args, **kwargs)

    @property
    def balance(self):
        return Decimal(self.balance_membership + self.balance_signup + self.balance_card)


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateTimeField('starts at')
    tournament = models.ForeignKey('Tournament')

    division_choices = (
        ('M', 'Men'),
        ('F', 'Ladies'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
        ('X', 'Mixed'),
        ('O', 'Open'),
    )
    division = models.CharField(max_length=1, choices=division_choices, default='M')
    format_choices = (
        ('S', 'Singles'),
        ('D', 'Doubles'),
        ('T', 'Triples'),
    )
    format = models.CharField(max_length=1, choices=format_choices, default='S')
    draw_choies = (
        ('L', 'Blind Draw'),
        ('D', 'Bring'),
    )
    draw = models.CharField(max_length=1, choices=draw_choies, default='D')
    game_choies = (
        ('CR', 'Cricket'),
        ('501', '501'),
        ('701', '701'),
        ('Medley', 'Medley'),
    )
    game = models.CharField(max_length=12, choices=game_choies, default='CR')
    category_choices = (
        ('S', 'Side Shoot'),
        ('O', 'Official')
        )
    category = models.CharField(max_length=1, choices=category_choices, default='O')

    def __unicode__(self):
        # return "%s/ %s / %s / %s" % (self.title, self.division_choices[self.division],
                                     # self.format_choices[self.format], self.game_choies[self.game])
        return self.title

    @property
    def signup_fee(self):
        return settings.FEES['SIGNUP'] if self.is_official() else settings.FEES['SIDESHOOT']

    def total_signup(self):
        if self.draw == 'L':
            return self.drawentry_set.all().count()
        elif self.draw == 'D':
            return self.team_set.all().count()
        else:
            return 0

    def is_lotd(self):
        return True if self.draw == 'L' else False

    def is_drawn(self):
        if self.draw != 'L':
            return True
        if Team.objects.filter(event=self).count():
            return True
        else:
            return False

    def draw_sms_sent(self):
        return SMSLog.objects.filter(event=self).exists()

    def is_side_shoot(self):
        return True if self.category == 'S' else False

    def is_official(self):
        return True if self.category == 'O' else False

    def team_size(self):
        if self.is_lotd() or self.format == 'S':
            return 1
        elif self.format == 'D':
            return 2
        elif self.format == 'T':
            return 3

    def is_team_event(self):
        return True if self.format == 'D' or self.format == 'T' else False
    
    def is_ladies_event(self):
        return True if self.division == 'F' else False

    def is_paid_by(self, player):
        return True if self.signuppayment_set.filter(player=player).exists() else False


class DrawEntry(models.Model):
    event = models.ForeignKey(Event)
    player = models.ForeignKey('Player')

    def __unicode__(self):
        return self.player.full_name

    class Meta:
        unique_together = (('event', 'player'))


class Team(models.Model):
    name = models.CharField(max_length=255, null=True)
    players = models.ManyToManyField('Player')
    event = models.ForeignKey(Event)
    mpr_rank = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    ppd_rank = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    mpr_event = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    ppd_event = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __unicode__(self):
        if self.name:
            _team_name = self.name
        else:
            player_list = self.players.all()
            _team_name = ','.join(player.last_name.title() for player in player_list) \
                        if len(player_list) > 1 else player_list[0].full_name
        return "%s - %s" % (_team_name, self.event.title)

    @property
    def team_name(self):
        if self.name:
            team_name = self.name
        else:
            player_list = self.players.all()
            team_name = ','.join(player.last_name.title() for player in player_list) \
                        if len(player_list) > 1 else player_list[0].full_name
        return team_name


class Card(models.Model):
    rfid = models.CharField(max_length=255, editable=False, unique=True)
    cardno = models.CharField(max_length=16, editable=False, unique=True)
    # used = models.DateTimeField(null=True)
    player = models.OneToOneField(Player)

    def __unicode__(self):
        return self.cardno

    def orginal_rfid(self):
        cursor = connections['hi'].cursor()
        cursor.execute("SELECT getorigrfid2(%s)", [self.rfid])
        r = cursor.fetchone()
        return r[0]

    def is_new(self):
        cursor = connections['hi'].cursor()
        cursor.execute("SELECT utime FROM checkrfid WHERE rfid=%s", [self.rfid])
        r = cursor.fetchone()
        return False if r[0] else True

    def live_stat(self):
        cursor = connections['hi'].cursor()
        cursor.execute("SELECT mpr_ta2, ppd_ta2 FROM useravg WHERE rfid=getorigrfid2(%s)", [self.rfid])
        r = cursor.fetchone()
        return {'mpr': r[0], 'ppd': r[1]}


class SignupPayment(models.Model):
    player = models.ForeignKey('Player')
    event = models.ForeignKey('Event')
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        if self.paid:
            return '%s paid for %s' % (self.player, self.event)
        else:
            return '%s need to pay for %s' % (self.player, self.event)



class PaymentItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __unicode__(self):
        return self.name


class SignupPackage(PaymentItem):
    signup_tickets = models.ManyToManyField('Event')

class Payment(models.Model):
    player = models.ForeignKey('Player')
    items = models.ManyToManyField('PaymentItem')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    pay_type_choices = (
        ('B', 'Cash'),
        ('C', 'Credit Card'),
        ('P', 'Paypal')
        )
    pay_type = models.CharField(max_length=1, choices=pay_type_choices, default='B')
    paid_at = models.DateTimeField(auto_now_add=True)

# class EventStat(models.Model):
#     userid = models.CharField(max_length=64, editable=False, primary_key=True)
#     rfid = models.CharField(max_length=64, null=True, editable=False, unique=True)
#     mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
#     ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


# class Ranking(models.Model):
#     userid = models.CharField(max_length=64, editable=False, primary_key=True)
#     rfid = models.CharField(max_length=64, null=True, editable=False, unique=True)
#     mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
#     ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Console(models.Model):
    no = models.CharField(max_length=16, primary_key=True)
    machid = models.CharField(max_length=16, unique=True)
    serial = models.CharField(max_length=5, unique=True)
    mac_address = models.CharField(max_length=12, unique=True)
    ip_address = models.IPAddressField(null=True)

    def __unicode__(self):
        return self.no


class Match(models.Model):
    event = models.ForeignKey(Event)
    team1 = models.ForeignKey(Team, related_name='team1')
    team2 = models.ForeignKey(Team, related_name='team2')
    winner = models.ForeignKey(Team, related_name='winned_by', null=True)
    console = models.ForeignKey(Console, related_name='played_with', null=True)
    created_at = models.DateTimeField('created at', editable=False, null=True)
    ended_at = models.DateTimeField('ended at', editable=False, null=True)

    def __unicode__(self):
        return '%s:%s vs %s' % (self.event, self.team1, self.team2)

    def save(self, *args, **kwargs):
        self.created_at = datetime.now() if not self.id else self.created_at
        super(Match, self).save(*args, **kwargs)

    def player_list(self):
        return [self.team1.players.all()] + [self.team2.players.all()]


class SMSLog(models.Model):
    event = models.ForeignKey(Event)
    category = models.CharField(max_length=64)
    sent_at = models.DateTimeField('created at', editable=False, null=True)

    def save(self, *args, **kwargs):
        self.sent_at = datetime.now() if not self.id else self.sent_at
        super(SMSLog, self).save(*args, **kwargs)


class PreRegPlayer(Player):
    credit = models.DecimalField('credit', max_digits=8, decimal_places=2, default=0.00)
    note = models.TextField('note', null=True)
    is_registered = models.NullBooleanField(null=True)

    def __unicode__(self):
        return self.full_name
