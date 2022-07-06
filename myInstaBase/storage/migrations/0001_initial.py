# Generated by Django 4.0.5 on 2022-07-05 20:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('video', models.FileField(blank=True, upload_to='video/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])])),
                ('image', models.ImageField(blank=True, upload_to='preview/')),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(blank=True, default=False)),
                ('deleted', models.BooleanField(blank=True, default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privateChatName', models.CharField(max_length=64)),
                ('lastOpenDate', models.DateTimeField(blank=True)),
                ('privateChat', models.BooleanField(blank=True, default=True)),
                ('name', models.CharField(blank=True, max_length=64)),
                ('privateRoomMembers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('privateRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.privateroom')),
            ],
        ),
        migrations.CreateModel(
            name='CommentsQuotations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('create_at', models.DateTimeField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('baseComment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.comments')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.video')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.video'),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/')),
                ('phone', models.CharField(blank=True, max_length=20, unique=True)),
                ('socialAcc', models.BooleanField(blank=True, default=False)),
                ('isEmailConfirmed', models.BooleanField(blank=True, default=False)),
                ('isPhoneConformed', models.BooleanField(blank=True, default=False)),
                ('phoneConfirmationCode', models.IntegerField(blank=True, max_length=6)),
                ('name', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
