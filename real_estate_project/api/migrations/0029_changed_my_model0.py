# Generated by Django 3.2.4 on 2025-03-25 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_changed_my_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choicemodel',
            old_name='v',
            new_name='vv',
        ),
    ]
