# Generated by Django 2.2.19 on 2021-04-04 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bango', '0005_auto_20210404_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='bango',
            name='biko',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
