# Generated by Django 4.2.6 on 2023-10-05 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('room_number', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('latest_message_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=100, null=True)),
                ('region_certification', models.CharField(default='N', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('images', models.ImageField(upload_to='post_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product_reserved', models.CharField(default='N', max_length=1)),
                ('product_sold', models.CharField(default='N', max_length=1)),
                ('view_num', models.PositiveIntegerField(default=0)),
                ('chat_num', models.PositiveIntegerField(default=0)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_messages', to=settings.AUTH_USER_MODEL)),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='dangun_app.chatroom')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='chatroom',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_rooms', to='dangun_app.post'),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='starter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='started_chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
