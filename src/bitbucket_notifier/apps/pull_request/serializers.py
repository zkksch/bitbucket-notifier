from rest_framework import serializers

from bitbucket_notifier.apps.pull_request import models
from bitbucket_notifier.apps.reviewer.serializers import ReviewerSerializer


class ReviewSerializer(serializers.ModelSerializer):

    reviewer = ReviewerSerializer(read_only=True, many=False)

    class Meta:
        model = models.Review

        fields = (
            'id',
            'created',
            'modified',
            'pull_request',
            'reviewer',
            'state',
        )

        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class PullRequestSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = models.PullRequest

        fields = (
            'id',
            'created',
            'modified',
            'external_id',
            'author',
            'url',
            'state',
            'reviews'
        )

        read_only_fields = (
            'id',
            'created',
            'modified',
            'external_id',
            'reviews'
        )


class NotificationReviewerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationReviewer

        fields = (
            'reviewer_email',
            'type',
        )


class NotificationSerializer(serializers.ModelSerializer):

    reviewers = NotificationReviewerSerializer(read_only=True, many=True)

    class Meta:
        model = models.Notification

        fields = (
            'id',
            'created',
            'modified',
            'pull_request_id',
            'pull_request_url',
            'pull_request_state',
            'author_email',
            'url',
            'reviewers',
        )

        read_only_fields = (
            'id',
            'created',
            'modified',
            'reviewers',
        )
