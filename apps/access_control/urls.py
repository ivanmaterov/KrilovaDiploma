from django.urls import path
from .views import (
    AccessControlListView,
    AccessControlCreateView,
    AccessControlDeleteView,
    AccessControlUpdateView,
    ImportAccessControlView,
)

urlpatterns = [
    path(
        '',
        AccessControlListView.as_view(),
    ),
    path(
        'access-control-create/',
        AccessControlCreateView.as_view(),
        name='access-control-create',
    ),
    path(
        'access-control-delete/<int:pk>',
        AccessControlDeleteView.as_view(),
        name='access-control-delete',
    ),
    path(
        'access-control-update/<int:pk>',
        AccessControlUpdateView.as_view(),
        name='access-control-update',
    ),
    path(
        'import-access-control/',
        ImportAccessControlView.as_view(),
        name='import-access-control',
    )
]
