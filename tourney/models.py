from django.db import models, connections
from datetime import datetime, timedelta
from django.contrib.localflavor.us.models import USStateField


class Tournament(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateField()
    end_at = models.DateField()
    players = models.ManyToManyField('Player', through='Entry')

    def __unicode__(self):
        return self.title

    def is_over(self):
        return (datetime.now() > self.end_at)

    def total_entry(self):
        return len(self.players.all())

    def remaining_entry(self):
        return 500 - self.total_entry()


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateTimeField('starts at')
    tournament = models.ForeignKey('Tournament')
    teams = models.ManyToManyField('Team')
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
        ('L', 'Luck of Draw'),
        ('D', 'Division'),
    )
    draw = models.CharField(max_length=1, choices=draw_choies, default='D')
    game_choies = (
        ('CR', 'Cricket'),
        ('501', '501'),
        ('701', '701'),
    )
    game = models.CharField(max_length=3, choices=game_choies, default='CR')

    def __unicode__(self):
        # return "%s/ %s / %s / %s" % (self.title, self.division_choices[self.division], 
                                     # self.format_choices[self.format], self.game_choies[self.game])
        return self.title

    def total_signup(self):
        len(self.teams.all)


class Team(models.Model):
    name = models.CharField(max_length=255, null=True)
    players = models.ManyToManyField('Player')


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

    @property
    def full_name(self):
        return '%s %s' % (self.first_name.title(), self.last_name.title())

    @property
    def card_number(self):
        return Card.objects.get(owned_id=self.id).cardno
        # return self.cardno

    @property
    def rfid(self):
        return Card.objects.get(owned_id=self.id).rfid

    def is_profile_valid(self):
        return True if self.card_number and self.phone and self.email and self.gender else False

    def is_web_member(self):
        return True if self.user_id else False

    def casual_stat(self):
        cursor = connections['hi'].cursor()
        cursor.execute("SELECT ppd_ta2, mpr_ta2 FROM useravg where rfid = getorigrfid2(%s)", [self.rfid])
        r = cursor.fetchone()
        return {'PPD': r[0], 'MPR': r[1]}

    def ranking(self):
        # cursor = connections['hi'].cursor()
        # cursor.execute("SELECT m_id FROM members where rfid = %s", [self.rfid])
        # r = cursor.fetchone()
        # ranking = Ranking.objects.get(pk=r[0])
        ranking = Ranking.objects.get(pk=self.user_id)
        return {'PPD': ranking.ppd, 'MPR': ranking.mpr}

    def event_stat(self):
        try:
            event_stat = EventStat.objects.get(pk=self.user_id)
        except:
            return {'PPD': None, 'MPR': None}
        return {'PPD': event_stat.ppd, 'MPR': event_stat.mpr}

    def is_membership_valid(self):
        latest_entry = self.entry_set.latest('created')
        exp_date = latest_entry.created + timedelta(days=90)
        if datetime.now() > exp_date:
            return False
        return True

    def membership_expire_at(self):
        latest_entry = self.entry_set.latest('created')
        exp_date = latest_entry.created + timedelta(days=90)
        return exp_date


class Card(models.Model):
    rfid = models.CharField(max_length=255, editable=False, unique=True)
    cardno = models.CharField(max_length=16, editable=False, unique=True)
    # used = models.DateTimeField(null=True)
    owned = models.ForeignKey(Player, null=True)

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
        if r[0]:
            return False
        else:
            return True


class Entry(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created = models.DateTimeField(editable=False)

    class Meta:
        unique_together = (('tournament', 'player'))

    def __unicode__(self):
        return "%s plays %s" % (self.player.full_name, self.tournament.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        super(Entry, self).save(*args, **kwargs)


class EventStat(models.Model):
    userid = models.CharField(max_length=64, editable=False, primary_key=True)
    rfid = models.CharField(max_length=64, null=True, editable=False, unique=True)
    mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Ranking(models.Model):
    userid = models.CharField(max_length=64, editable=False, primary_key=True)
    rfid = models.CharField(max_length=64, null=True, editable=False, unique=True)
    mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
