# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profesor'
        db.create_table('app_base_profesor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('RUT', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('instituto', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('app_base', ['Profesor'])

        # Adding model 'ProfesorEvaluador'
        db.create_table('app_base_profesorevaluador', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profesor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_base.Profesor'])),
            ('instancia_ramo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_base.InstanciaRamo'])),
            ('colaborador', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app_base', ['ProfesorEvaluador'])

        # Adding model 'Ramo'
        db.create_table('app_base_ramo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('instituto', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('app_base', ['Ramo'])

        # Adding model 'InstanciaRamo'
        db.create_table('app_base_instanciaramo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ramo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_base.Ramo'])),
            ('agno', self.gf('django.db.models.fields.IntegerField')()),
            ('semestre', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('grupo', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('app_base', ['InstanciaRamo'])

        # Adding model 'Alumno'
        db.create_table('app_base_alumno', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('RUT', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('app_base', ['Alumno'])

        # Adding model 'Inscripcion'
        db.create_table('app_base_inscripcion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instancia_ramo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_base.InstanciaRamo'])),
            ('alumno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app_base.Alumno'])),
            ('grupo_por_defecto', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('app_base', ['Inscripcion'])

        # Adding model 'Ayudante'
        db.create_table('app_base_ayudante', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('RUT', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('app_base', ['Ayudante'])

        # Adding M2M table for field ramos on 'Ayudante'
        db.create_table('app_base_ayudante_ramos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ayudante', models.ForeignKey(orm['app_base.ayudante'], null=False)),
            ('instanciaramo', models.ForeignKey(orm['app_base.instanciaramo'], null=False))
        ))
        db.create_unique('app_base_ayudante_ramos', ['ayudante_id', 'instanciaramo_id'])


    def backwards(self, orm):
        # Deleting model 'Profesor'
        db.delete_table('app_base_profesor')

        # Deleting model 'ProfesorEvaluador'
        db.delete_table('app_base_profesorevaluador')

        # Deleting model 'Ramo'
        db.delete_table('app_base_ramo')

        # Deleting model 'InstanciaRamo'
        db.delete_table('app_base_instanciaramo')

        # Deleting model 'Alumno'
        db.delete_table('app_base_alumno')

        # Deleting model 'Inscripcion'
        db.delete_table('app_base_inscripcion')

        # Deleting model 'Ayudante'
        db.delete_table('app_base_ayudante')

        # Removing M2M table for field ramos on 'Ayudante'
        db.delete_table('app_base_ayudante_ramos')


    models = {
        'app_base.alumno': {
            'Meta': {'object_name': 'Alumno'},
            'RUT': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'app_base.ayudante': {
            'Meta': {'object_name': 'Ayudante'},
            'RUT': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ramos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_base.InstanciaRamo']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'app_base.inscripcion': {
            'Meta': {'object_name': 'Inscripcion'},
            'alumno': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_base.Alumno']"}),
            'grupo_por_defecto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_ramo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_base.InstanciaRamo']"})
        },
        'app_base.instanciaramo': {
            'Meta': {'object_name': 'InstanciaRamo'},
            'agno': ('django.db.models.fields.IntegerField', [], {}),
            'grupo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ramo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_base.Ramo']"}),
            'semestre': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'app_base.profesor': {
            'Meta': {'object_name': 'Profesor'},
            'RUT': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instituto': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'app_base.profesorevaluador': {
            'Meta': {'object_name': 'ProfesorEvaluador'},
            'colaborador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instancia_ramo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_base.InstanciaRamo']"}),
            'profesor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_base.Profesor']"})
        },
        'app_base.ramo': {
            'Meta': {'object_name': 'Ramo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instituto': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app_base']