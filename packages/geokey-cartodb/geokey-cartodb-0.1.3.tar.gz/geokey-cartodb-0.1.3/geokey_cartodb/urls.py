from django.conf.urls import url

from views import (
    IndexPage, ProjectDataView
)

urlpatterns = [
    url(
        r'^admin/cartodb/$',
        IndexPage.as_view(),
        name='index'),
    url(
        r'^api/cartodb/projects/(?P<project_id>[0-9]+)$',
        ProjectDataView.as_view(),
        name='project_data')
]
