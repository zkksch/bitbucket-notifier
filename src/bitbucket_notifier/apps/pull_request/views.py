from django.db.transaction import atomic
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bitbucket_notifier.apps.pull_request import models
from bitbucket_notifier.apps.pull_request import serializers


class PullRequestsViewSet(viewsets.ModelViewSet):
    queryset = models.PullRequest.objects.all()
    serializer_class = serializers.PullRequestSerializer

    permission_classes = (permissions.IsAdminUser,)

    @action(detail=False, methods=['post'])
    @atomic
    def notify(self, request):
        notification_serializer = serializers.NotificationSerializer(
            data=request.data)

        reviewers = [
            {
                'reviewer_email': email,
                'type': models.NotificationReviewer.ADDED
            }
            for email in request.data['reviewers']
        ]

        reviewers_approved = [
            {
                'reviewer_email': email,
                'type': models.NotificationReviewer.APPROVED
            }
            for email in request.data['reviewers_approved']
        ]

        reviewers_needs_work = [
            {
                'reviewer_email': email,
                'type': models.NotificationReviewer.NEEDS_WORK
            }
            for email in request.data['reviewers_needs_work']
        ]

        if notification_serializer.is_valid():
            notification = notification_serializer.save()

            for nr_list in (reviewers,
                            reviewers_approved,
                            reviewers_needs_work):
                for nr in nr_list:
                    nr_serializer = serializers.NotificationReviewerSerializer(
                        data=nr)

                    if nr_serializer.is_valid():
                        nr_serializer.save(
                            notification=notification
                        )
                    else:
                        return Response(
                            nr_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST
                        )

            pull_request = models.PullRequest.objects.handle_notification(
                notification)

            return Response({
                'status': 'Notification processed successfully',
                'pull_request_id': pull_request.pk
            })
        else:
            return Response(
                notification_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    permission_classes = (permissions.IsAdminUser,)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    permission_classes = (permissions.IsAdminUser,)
