# Generated by Django 4.2.4 on 2023-08-26 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_person_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='interests',
            field=models.CharField(default='React', max_length=50),
            preserve_default=False,
        ),
    ]