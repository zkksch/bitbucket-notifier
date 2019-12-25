# Generated by Django 3.0.1 on 2019-12-25 08:38

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('pull_request', '0005_auto_20191225_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pullrequest',
            name='state',
            field=models.CharField(choices=[('OPEN', 'Opened'), ('MERGED', 'Merged'), ('DECLINED', 'Declined'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=32, verbose_name='State'),
        ),
    ]
