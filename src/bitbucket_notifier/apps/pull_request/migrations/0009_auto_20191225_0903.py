# Generated by Django 3.0.1 on 2019-12-25 09:03

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('pull_request', '0008_auto_20191225_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationreviewer',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='pull_request.Notification'),
        ),
    ]
