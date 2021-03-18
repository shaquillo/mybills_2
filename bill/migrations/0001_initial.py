# Generated by Django 3.0.8 on 2021-03-18 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enterprise', '__first__'),
        ('profiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('userReceptionDate', models.DateField(auto_now_add=True)),
                ('paymentDateLimit', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Client')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprise.Enterprise')),
            ],
            options={
                'ordering': ['creationDate'],
            },
        ),
    ]
