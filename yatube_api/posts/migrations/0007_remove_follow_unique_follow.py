# Generated by Django 3.2.16 on 2024-09-23 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_follow_unique_follow'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
    ]
