from rest_framework import permissions
from rest_framework import viewsets

from bitbucket_notifier.apps.reviewer import models
from bitbucket_notifier.apps.reviewer import serializers


class ReviewerViewSet(viewsets.ModelViewSet):
    queryset = models.Reviewer.objects.all()
    serializer_class = serializers.ReviewerSerializer

    permission_classes = (permissions.IsAdminUser,)
