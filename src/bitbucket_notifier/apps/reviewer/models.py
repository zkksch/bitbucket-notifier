from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bitbucket_notifier.core.models import ObjectModel


class ReviewerQuerySet(models.QuerySet):
    """
    Reviewer QuerySet
    """
    def find(self, email):
        """
        Find reviewer (or create if necessary)

        :param email: Reviewer email
        :return: Reviewer object
        """
        reviewer, __ = self.get_or_create(email=email)
        return reviewer


class Reviewer(ObjectModel):
    """
    Reviewer model

    Reviewers will be bounded with bitbucket users via email value
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('System user'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        blank=True,
        null=True,
    )

    telegram_username = models.CharField(
        verbose_name=_('Telegram username'),
        max_length=32,
        blank=True,
        null=True,
        unique=True
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        blank=False,
        null=False,
        unique=True
    )

    objects = ReviewerQuerySet.as_manager()
