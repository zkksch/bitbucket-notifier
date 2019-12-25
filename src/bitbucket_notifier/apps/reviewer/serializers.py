from rest_framework import serializers

from bitbucket_notifier.apps.reviewer import models


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviewer

        fields = (
            'id',
            'created',
            'modified',
            'user',
            'name',
            'telegram_username',
            'email',
        )

        read_only_fields = (
            'id',
            'created',
            'modified',
        )
