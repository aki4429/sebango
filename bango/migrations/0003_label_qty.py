# Generated by Django 2.2.19 on 2021-03-14 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bango', '0002_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='qty',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]
