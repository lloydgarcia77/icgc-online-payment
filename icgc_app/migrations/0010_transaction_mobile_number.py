# Generated by Django 3.2.14 on 2022-09-10 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icgc_app', '0009_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]