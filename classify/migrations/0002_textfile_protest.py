# Generated by Django 2.0.7 on 2018-07-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textfile',
            name='protest',
            field=models.BooleanField(default=False),
        ),
    ]
