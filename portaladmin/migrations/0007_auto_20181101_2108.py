# Generated by Django 2.1.1 on 2018-11-01 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portaladmin', '0006_auto_20181031_1302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mdstatementhistory',
            options={'verbose_name': 'Metadaten Statement History'},
        ),
        migrations.RemoveField(
            model_name='mdstatement',
            name='Validation_message',
        ),
        migrations.RemoveField(
            model_name='mdstatementhistory',
            name='Validation_message',
        ),
        migrations.AddField(
            model_name='mdstatement',
            name='validation_message',
            field=models.CharField(blank=True, db_column='validation_message', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='mdstatementhistory',
            name='validation_message',
            field=models.CharField(blank=True, db_column='validation_message', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='mdstatement',
            name='Status',
            field=models.CharField(choices=[('created', 'erstellt'), ('uploaded', 'hochgeladen'), ('request_queue', 'signiert und eingebracht'), ('rejected', 'fehlerhaft'), ('accepted', 'akzeptiert')], default='uploaded', max_length=14, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='mdstatementhistory',
            name='Status',
            field=models.CharField(choices=[('created', 'erstellt'), ('uploaded', 'hochgeladen'), ('request_queue', 'signiert und eingebracht'), ('rejected', 'fehlerhaft'), ('accepted', 'akzeptiert')], default='uploaded', max_length=14, null=True, verbose_name='Status'),
        ),
    ]
