from django.contrib.auth.models import User

from dmethylation.models import Region, IlluminaMethylation450, CpGHasTranscriptRegions


def create_superuser(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return User.objects.create_superuser(**defaults)


def create_region(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Region.objects.create(**defaults)


def create_illuminamethylation450(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return IlluminaMethylation450.objects.create(**defaults)


def create_cpghastranscriptregions(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return CpGHasTranscriptRegions.objects.create(**defaults)
