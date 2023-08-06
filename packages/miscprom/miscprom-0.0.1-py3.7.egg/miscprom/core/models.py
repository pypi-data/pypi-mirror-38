from django.db import models
from pkg_resources import working_set


def choices():
    for entry in working_set.iter_entry_points('exporter'):
        yield entry.module_name, entry.name


class ApiKey(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='+',
        help_text='Django user object'
    )
    service = models.CharField(
        max_length=64,
        help_text='Service identifier',
        choices=choices(),
    )
    key = models.CharField(
        max_length=60,
        help_text='Service API Key'
    )
