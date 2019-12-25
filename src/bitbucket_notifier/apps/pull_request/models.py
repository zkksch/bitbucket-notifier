from django.db import models
from django.utils.translation import ugettext_lazy as _

from bitbucket_notifier.apps.reviewer.models import Reviewer
from bitbucket_notifier.core.models import BaseModel
from bitbucket_notifier.core.models import ObjectModel

from .constants import *


class PullRequestQuerySet(models.QuerySet):
    """
    Pull request QuerySet
    """
    def handle_notification(self, notification):
        """
        Handle bitbucket notification

        :param notification: Notification
        :return: Affected pull request
        """
        author = Reviewer.objects.find(notification.author_email)

        state = {
            'OPEN': STATE_OPEN,
            'MERGED': STATE_MERGED,
            'DECLINED': STATE_DECLINED,
        }.get(notification.pull_request_state, STATE_UNKNOWN)

        try:
            pull_request = self.get(
                external_id=notification.pull_request_id)
        except self.model.DoesNotExist:
            pull_request = self.create(
                external_id=notification.pull_request_id,
                author=author,
                url=notification.pull_request_url
            )

        pull_request.state = state

        for notification_reviewer in notification.added_reviewers:
            email = notification_reviewer.reviewer_email
            reviewer = Reviewer.objects.find(email)

            review, _ = Review.objects.get_or_create(
                pull_request=pull_request, reviewer=reviewer)

            if notification.reviewers_approved.filter(
                    reviewer_email=email).exists():
                review.state = REVIEW_APPROVED
            elif notification.reviewers_needs_work.filter(
                    reviewer_email=email).exists():
                review.state = REVIEW_NEEDS_WORK
            else:
                review.state = None

            review.save()

        pull_request.save()

        return pull_request


class PullRequest(ObjectModel):
    """
    Pull request model
    """

    STATE_CHOICES = (
        (STATE_OPEN, _('Opened')),
        (STATE_MERGED, _('Merged')),
        (STATE_DECLINED, _('Declined')),
        (STATE_UNKNOWN, _('Unknown')),
    )

    external_id = models.PositiveIntegerField(
        verbose_name=_('External ID'),
        blank=False,
        null=False,
        unique=True
    )

    author = models.ForeignKey(
        Reviewer,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    url = models.CharField(
        verbose_name=_('URL'),
        max_length=2000,
        blank=False,
        null=False,
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=32,
        blank=False,
        null=False,
        default=STATE_UNKNOWN,
        choices=STATE_CHOICES
    )

    reviewers = models.ManyToManyField(
        Reviewer,
        through='pull_request.Review',
        related_name='reviewing_pull_requests'
    )

    objects = PullRequestQuerySet.as_manager()


class Review(ObjectModel):
    """
    Pull request review model

    M2M between PR and reviewer
    """

    STATE_CHOICES = (
        (REVIEW_APPROVED, _('Approved')),
        (REVIEW_NEEDS_WORK, _('Needs work'))
    )

    pull_request = models.ForeignKey(
        PullRequest,
        verbose_name=_('Pull request'),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='reviews'
    )

    reviewer = models.ForeignKey(
        Reviewer,
        verbose_name=_('Reviewer'),
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name='reviews'
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=32,
        blank=False,
        null=True,
        choices=STATE_CHOICES
    )

    class Meta:
        unique_together = ('pull_request', 'reviewer')


class Notification(ObjectModel):
    pull_request_id = models.PositiveIntegerField(
        verbose_name=_('Pull request external ID'),
        blank=False,
        null=False
    )

    pull_request_url = models.URLField(
        verbose_name=_('Pull request URL'),
        blank=False,
        null=False
    )

    pull_request_state = models.CharField(
        verbose_name=_('Pull request state'),
        max_length=32,
        blank=False,
        null=False
    )

    author_email = models.EmailField(
        verbose_name=_('Author email'),
        blank=False,
        null=False
    )

    @property
    def added_reviewers(self):
        """
        All reviewers from pull request notification

        :return: Reviewers list
        """
        return self.notificationreviewer_set.filter(
            type=NotificationReviewer.ADDED
        )

    @property
    def reviewers_approved(self):
        """
        Reviewers that marked PR as "approved" from pull request
        notification

        :return: Reviewers list
        """
        return self.notificationreviewer_set.filter(
            type=NotificationReviewer.APPROVED
        )

    @property
    def reviewers_needs_work(self):
        """
        Reviewers that marked PR as "needs work" from pull request
        notification

        :return: Reviewers list
        """
        return self.notificationreviewer_set.filter(
            type=NotificationReviewer.NEEDS_WORK
        )


class NotificationReviewer(BaseModel):
    """
    Reviewers from notification
    """

    ADDED = 'ADDED'
    APPROVED = 'APPROVED'
    NEEDS_WORK = 'NEEDS_WORK'

    TYPE_CHOICES = (
        (ADDED, _('Added')),
        (APPROVED, _('Approved')),
        (NEEDS_WORK, _('Needs work')),
    )

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='reviewers'
    )

    reviewer_email = models.EmailField(
        verbose_name=_('Reviewer email'),
        blank=False,
        null=False
    )

    type = models.CharField(
        verbose_name=_('Reviewer type'),
        max_length=32,
        blank=False,
        null=False,
        choices=TYPE_CHOICES
    )
