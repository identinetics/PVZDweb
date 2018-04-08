# Generated by Django 2.0.3 on 2018-03-21 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0003_auto_20180321_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gvfederationorg',
            name='gvCaseNumber',
            field=models.CharField(blank=True, help_text='Geschäftszahl(en) für Antrag, Vertrag und Änderungen', max_length=500, null=True, verbose_name='Geschäftszahl(en)'),
        ),
        migrations.AlterField(
            model_name='gvfederationorg',
            name='gvFederationNames',
            field=models.ForeignKey(blank=True, default='portalverbund.gv.at', help_text='Vertrag mit Federation', null=True, on_delete=django.db.models.deletion.CASCADE, to='tnadmin.GvFederation', verbose_name='Federation'),
        ),
    ]