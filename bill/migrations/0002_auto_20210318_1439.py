# Generated by Django 3.0.8 on 2021-03-18 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_worker_is_admin'),
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='client',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='enterprise',
        ),
        migrations.AddField(
            model_name='bill',
            name='subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='profiles.Subscription'),
        ),
    ]
