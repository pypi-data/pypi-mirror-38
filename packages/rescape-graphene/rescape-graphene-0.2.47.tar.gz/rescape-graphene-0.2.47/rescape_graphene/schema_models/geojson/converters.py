
from django.contrib.gis.db import models

import graphene
from graphene_django.converter import convert_django_field

from rescape_graphene.schema_models.geojson.types import GeometryCollectionType

@convert_django_field.register(models.GeometryCollectionField)
def convert_field_to_geometry_collection(field, registry=None):
    return graphene.Field(
        GeometryCollectionType,
        description=field.help_text,
        required=not field.null)