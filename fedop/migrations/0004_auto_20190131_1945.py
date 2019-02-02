# Generated by Django 2.1.4 on 2019-01-31 18:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fedop', '0003_gvorg_policyjournal'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GvOrg_PolicyJournal',
        ),
        migrations.AddField(
            model_name='issuer',
            name='added_to_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='issuer',
            name='deleted_from_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='namespaceobj',
            name='added_to_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='namespaceobj',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 169931, tzinfo=utc), verbose_name='Eingangsdatum'),
        ),
        migrations.AddField(
            model_name='namespaceobj',
            name='deleted_from_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='namespaceobj',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 170018, tzinfo=utc), verbose_name='Änderungsdatum'),
        ),
        migrations.AddField(
            model_name='revocation',
            name='added_to_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revocation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 169931, tzinfo=utc), verbose_name='Eingangsdatum'),
        ),
        migrations.AddField(
            model_name='revocation',
            name='deleted_from_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revocation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 170018, tzinfo=utc), verbose_name='Änderungsdatum'),
        ),
        migrations.AddField(
            model_name='userprivilege',
            name='added_to_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprivilege',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 169931, tzinfo=utc), verbose_name='Eingangsdatum'),
        ),
        migrations.AddField(
            model_name='userprivilege',
            name='deleted_from_journal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprivilege',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 170018, tzinfo=utc), verbose_name='Änderungsdatum'),
        ),
        migrations.AlterField(
            model_name='issuer',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 169931, tzinfo=utc), verbose_name='Eingangsdatum'),
        ),
        migrations.AlterField(
            model_name='issuer',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 31, 18, 45, 11, 170018, tzinfo=utc), verbose_name='Änderungsdatum'),
        ),
    ]
