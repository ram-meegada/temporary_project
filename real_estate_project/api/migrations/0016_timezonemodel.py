# Generated by Django 3.2.4 on 2025-02-03 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_modelb_mo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeZoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
