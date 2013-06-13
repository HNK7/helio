# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PreRegPlayer.is_registered'
        db.add_column('tourney_preregplayer', 'is_registered', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PreRegPlayer.is_registered'
        db.delete_column('tourney_preregplayer', 'is_registered')


    models = {
        'tourney.card': {
            'Meta': {'object_name': 'Card'},
            'cardno': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Player']"}),
            'rfid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'tourney.console': {
            'Meta': {'object_name': 'Console'},
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tourney.drawentry': {
            'Meta': {'unique_together': "(('event', 'player'),)", 'object_name': 'DrawEntry'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Player']"})
        },
        'tourney.entry': {
            'Meta': {'unique_together': "(('tournament', 'player'),)", 'object_name': 'Entry'},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpr_event': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'}),
            'mpr_rank': ('django.db.models.fields.DecimalField', [], {'default': '9.0', 'max_digits': '3', 'decimal_places': '2'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Player']"}),
            'ppd_event': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'ppd_rank': ('django.db.models.fields.DecimalField', [], {'default': '60', 'max_digits': '5', 'decimal_places': '2'}),
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
        'tourney.match': {
            'Meta': {'object_name': 'Match'},
            'console': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'played_with'", 'null': 'True', 'to': "orm['tourney.Console']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team1'", 'to': "orm['tourney.Team']"}),
            'team2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team2'", 'to': "orm['tourney.Team']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winned_by'", 'null': 'True', 'to': "orm['tourney.Team']"})
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
        'tourney.preregplayer': {
            'Meta': {'object_name': 'PreRegPlayer', '_ormbases': ['tourney.Player']},
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'is_registered': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'player_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tourney.Player']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tourney.smslog': {
            'Meta': {'object_name': 'SMSLog'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'tourney.team': {
            'Meta': {'object_name': 'Team'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tourney.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpr_event': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'}),
            'mpr_rank': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tourney.Player']", 'symmetrical': 'False'}),
            'ppd_event': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'ppd_rank': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'})
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
