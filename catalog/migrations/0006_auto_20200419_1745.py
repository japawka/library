# Generated by Django 3.0.5 on 2020-04-19 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20200419_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'permissions': (('can_mark_returned', 'Set book as OK'),)},
        ),
    ]