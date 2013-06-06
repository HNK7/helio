# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tournament'
        db.create_table('tourney_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_at', self.gf('django.db.models.fields.DateField')()),
            ('end_at', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('tourney', ['Tournament'])

        # Adding model 'Event'
        db.create_table('tourney_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourney.Tournament'])),
            ('division', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('format', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
            ('draw', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('game', self.gf('django.db.models.fields.CharField')(default='CR', max_length=3)),
        ))
        db.send_create_signal('tourney', ['Event'])

        # Adding M2M table for field teams on 'Event'
        db.create_table('tourney_event_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['tourney.event'], null=False)),
            ('team', models.ForeignKey(orm['tourney.team'], null=False))
        ))
        db.create_unique('tourney_event_teams', ['event_id', 'team_id'])

        # Adding model 'Team'
        db.create_table('tourney_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('tourney', ['Team'])

        # Adding M2M table for field players on 'Team'
        db.create_table('tourney_team_players', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['tourney.team'], null=False)),
            ('player', models.ForeignKey(orm['tourney.player'], null=False))
        ))
        db.create_unique('tourney_team_players', ['team_id', 'player_id'])

        # Adding model 'Player'
        db.create_table('tourney_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street_line1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('street_line2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='US', max_length=100, null=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('registered_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tourney', ['Player'])

        # Adding model 'Card'
        db.create_table('tourney_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('cardno', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('owned', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourney.Player'], null=True)),
        ))
        db.send_create_signal('tourney', ['Card'])

        # Adding model 'Entry'
        db.create_table('tourney_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourney.Tournament'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourney.Player'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('tourney', ['Entry'])

        # Adding unique constraint on 'Entry', fields ['tournament', 'player']
        db.create_unique('tourney_entry', ['tournament_id', 'player_id'])

        # Adding model 'EventStat'
        db.create_table('tourney_eventstat', (
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True)),
            ('mpr', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2)),
            ('ppd', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('tourney', ['EventStat'])

        # Adding model 'Ranking'
        db.create_table('tourney_ranking', (
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True)),
            ('mpr', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2)),
            ('ppd', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('tourney', ['Ranking'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Entry', fields ['tournament', 'player']
        db.delete_unique('tourney_entry', ['tournament_id', 'player_id'])

        # Deleting model 'Tournament'
        db.delete_table('tourney_tournament')

        # Deleting model 'Event'
        db.delete_table('tourney_event')

        # Removing M2M table for field teams on 'Event'
        db.delete_table('tourney_event_teams')

        # Deleting model 'Team'
        db.delete_table('tourney_team')

        # Removing M2M table for field players on 'Team'
        db.delete_table('tourney_team_players')

        # Deleting model 'Player'
        db.delete_table('tourney_player')

        # Deleting model 'Card'
        db.delete_table('tourney_card')

        # Deleting model 'Entry'
        db.delete_table('tourney_entry')

        # Deleting model 'EventStat'
        db.delete_table('tourney_eventstat')

        # Deleting model 'Ranking'
        db.delete_table('tourney_ranking')


    models = {
        'tourney.card': {
            'Meta': {'object_name': 'Card'},
            'cardno': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owned': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Player']", 'null': 'True'}),
            'rfid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'tourney.entry': {
            'Meta': {'unique_together': "(('tournament', 'player'),)", 'object_name': 'Entry'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Player']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Tournament']"})
        },
        'tourney.event': {
            'Meta': {'object_name': 'Event'},
            'division': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'draw': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'game': ('django.db.models.fields.CharField', [], {'default': "'CR'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tourney.Team']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Tournament']"})
        },
        'tourney.eventstat': {
            'Meta': {'object_name': 'EventStat'},
            'mpr': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'ppd': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'rfid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'tourney.player': {
            'Meta': {'object_name': 'Player'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'street_line1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'street_line2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'tourney.ranking': {
            'Meta': {'object_name': 'Ranking'},
            'mpr': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'ppd': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'rfid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'tourney.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tourney.Player']", 'symmetrical': 'False'})
        },
        'tourney.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'end_at': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tourney.Player']", 'through': "orm['tourney.Entry']", 'symmetrical': 'False'}),
            'start_at': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['tourney']
