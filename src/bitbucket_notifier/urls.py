import json
from os.path import dirname
from os.path import join

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from bitbucket_notifier.apps.pull_request import views as pull_request_views
from bitbucket_notifier.apps.reviewer import views as reviewer_views


with open(join(dirname(settings.BASE_DIR), 'meta.json'), mode='r') as meta:
    meta_info = json.load(meta)


router = routers.DefaultRouter()

router.register(r'reviewer',
                reviewer_views.ReviewerViewSet)
router.register(r'pull-request',
                pull_request_views.PullRequestsViewSet)
router.register(r'review',
                pull_request_views.ReviewViewSet)
router.register(r'notification',
                pull_request_views.NotificationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    path('openapi', get_schema_view(
        title=meta_info['name'],
        description=meta_info['description'],
        version=meta_info['version']
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='doc'),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework'))
]
