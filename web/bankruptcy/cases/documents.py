from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Case


@registry.register_document
class CaseDocument(Document):
    class Index:
        name = 'cases' 
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Case # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'recap_id',
            'pacer_id',
            'jurisdiction',
            'chapter',
        ]

        # Auto update Elasticsearch when a model is saved
        # or deleted:
        ignore_signals = False

        # Perform an index refresh after every update (overrides global setting):
        auto_refresh = True

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000