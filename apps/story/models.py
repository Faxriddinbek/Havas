from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from apps.shared.models import BaseModel

class StoryTestModel(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    variant_1 = models.CharField(max_length=255)
    variant_2 = models.CharField(max_length=255)
    variant_3 = models.CharField(max_length=255)
    variant_4 = models.CharField(max_length=255)

class StoryModel(BaseModel):
    media_files = GenericRelation(
        'shared.Media',
        related_query_name='products'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    test = models.ForeignKey(StoryTestModel, on_delete=models.CASCADE, null=True, blank=True, related_name='story_test')
