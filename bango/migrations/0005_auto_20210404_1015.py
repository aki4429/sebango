# Generated by Django 2.2.19 on 2021-04-04 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bango', '0004_auto_20210315_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='bango',
            name='kikaku',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bango',
            name='hcode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
