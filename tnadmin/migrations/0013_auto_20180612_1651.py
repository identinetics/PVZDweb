# Generated by Django 2.0.3 on 2018-06-12 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0012_auto_20180427_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gvorganisation',
            name='gvOuID',
            field=models.CharField(db_column='gvOuVKZ', help_text='Syntax: gvOuID::= Landeskennung ":" ID ID::= "VKZ:" VKZ | Org-Id  (z.B. AT:VKZ:GGA1234, AT:L9:9876)', max_length=32, unique=True, verbose_name='gvOuId'),
        ),
        migrations.AlterField(
            model_name='gvorganisation',
            name='gvOuVKZ',
            field=models.CharField(db_column='gvOuID', help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium) \u2028(z.B. GGA-12345)', max_length=32, unique=True, verbose_name='Verwaltungskennz (gvOuVKZ)'),
        ),
        migrations.AlterField(
            model_name='gvorgunit',
            name='gvOuID',
            field=models.CharField(db_column='gvOuVKZ', help_text='Syntax: gvOuID::= Landeskennung ":" ID ID::= "VKZ:" VKZ | Org-Id  (z.B. AT:VKZ:GGA1234, AT:L9:9876)', max_length=32, unique=True, verbose_name='gvOuId'),
        ),
        migrations.AlterField(
            model_name='gvorgunit',
            name='gvOuVKZ',
            field=models.CharField(db_column='gvOuID', help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium) \u2028(z.B. GGA-12345)', max_length=32, unique=True, verbose_name='Verwaltungskennz (gvOuVKZ)'),
        ),
    ]
