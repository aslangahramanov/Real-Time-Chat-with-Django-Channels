# Generated by Django 4.2.4 on 2023-08-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_person_interests_delete_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='unique_id',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
