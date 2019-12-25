from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """
    Base model
    """

    def __str__(self):
        return f'{self.__class__.__name__} (id={self.pk})'

    class Meta:
        abstract = True


class WithCreatedModel(BaseModel):
    """
    Model with created field
    """

    created = models.DateTimeField(
        _('Created'), auto_now_add=True, null=False, blank=False)

    class Meta:
        abstract = True


class WithModifiedModel(BaseModel):
    """
    Model with modified field
    """

    modified = models.DateTimeField(
        _('Modified'), auto_now=True, null=False, blank=False)

    class Meta:
        abstract = True


class ObjectModel(WithCreatedModel, WithModifiedModel):
    """
    Model for entities
    """

    class Meta:
        abstract = True
