# Generated by Django 3.2.4 on 2025-03-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptop', '0004_changed_my_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='FloatDecimalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f', models.FloatField()),
                ('d', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
    ]
