# Generated by Django 3.2.4 on 2025-02-03 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_timezonemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='timezonemodel',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
