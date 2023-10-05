# Generated by Django 4.2.5 on 2023-09-27 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('user_id', models.CharField(max_length=50)),
                ('product_id', models.IntegerField()),
                ('chatting', models.TextField(null=True)),
                ('chatting_num', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(default='oreumi', max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('product_description', models.TextField()),
                ('deal_location', models.CharField(max_length=100)),
                ('product_img', models.ImageField(upload_to='product_img/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
