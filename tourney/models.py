from django.db import models
from datetime import datetime


class Tournament(models.Model):
    title = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    players = models.ManyToManyField('Player', through='Entry')

    def __unicode__(self):
        return self.title

    def is_over(self):
        return (datetime.now() > self.end_at)


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
    )
    division = models.CharField(max_length=1, choices=division_choices, default='M')
    format_choices = (
        ('S', 'Singles'),
        ('D', 'Doubles'),
        ('T', 'Triples'),
    )
    format = models.CharField(max_length=1, choices=format_choices, default='S')
    draw_choies = (
        ('D', 'Division'),
        ('L', 'Luck of Draw'),
    )
    draw = models.CharField(max_length=1, choices=draw_choies, default='D')
    game_choies = (
        ('501', '501'),
        ('701', '701'),
        ('CR', 'Cricket'),
    )
    game = models.CharField(max_length=3, choices=game_choies)

    def __unicode__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=255)
    players = models.ManyToManyField('Player')

    def __unicode__(self):
        return self.name


class Player(models.Model):
    gender_choices = (
        ('M', 'M'),
        ('F', 'F'),
    )
    cardno = models.CharField(max_length=16, null=True)
    rfid = models.CharField(max_length=64, null=True, editable=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, choices=gender_choices, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=40, null=True)
    street_line1 = models.CharField(max_length=100, null=True)
    street_line2 = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True, default='US')
    # registered_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.full_name()

    def full_name(self):

        return '%s %s' % (self.first_name, self.last_name)

    def phone_number(self):
        return '(%s%s%s) %s%s%s-%s%s%s%s' % tuple(self.phone)

    def card_number(self):
        # return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(self.cardno) if self.cardno else None
        return self.cardno

    def is_profile_valid(self):
        return True if self.cardno and self.phone and self.email and self.gender else False


class Entry(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.player.full_name()


class EventStat(models.Model):
    mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    player = models.ForeignKey(Player)
    event = models.ForeignKey(Event)


class Ranking(models.Model):
    mpr = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ppd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    player = models.ForeignKey(Player)
