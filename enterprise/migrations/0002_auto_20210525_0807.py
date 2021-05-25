# Generated by Django 3.0.8 on 2021-05-25 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='enterprise'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]