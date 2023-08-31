# Generated by Django 4.2.4 on 2023-08-29 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_personimage_delete_mymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='interests',
        ),
        migrations.AddField(
            model_name='person',
            name='interests',
            field=models.ManyToManyField(to='chat.interest'),
        ),
    ]