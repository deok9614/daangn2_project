# Generated by Django 4.2.5 on 2023-09-19 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dangun_app', '0008_chat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like_num',
            new_name='view_num',
        ),
    ]
