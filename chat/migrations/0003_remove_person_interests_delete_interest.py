# Generated by Django 4.2.4 on 2023-08-26 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_interest_person_delete_visitortoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='interests',
        ),
        migrations.DeleteModel(
            name='Interest',
        ),
    ]
