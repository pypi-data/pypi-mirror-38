import graphene

from graphene_django.types import DjangoObjectType, DjangoObjectTypeOptions
from .paginator import Paginator

# todo: is this the best way to do this?
from .converter import *  # noqa


class BaseDjangoObjectType(DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, **options):
        if not _meta:
            _meta = DjangoObjectTypeOptions(cls)

        PageMeta = {'description': cls.__name__}
        PageClass = type('{}Paginator'.format(cls.__name__), (Paginator,), {'Meta': PageMeta,
                                                                            'object_list': graphene.List(cls)})
        _meta.paginator = PageClass

        super(BaseDjangoObjectType, cls).__init_subclass_with_meta__(_meta=_meta, **options)
