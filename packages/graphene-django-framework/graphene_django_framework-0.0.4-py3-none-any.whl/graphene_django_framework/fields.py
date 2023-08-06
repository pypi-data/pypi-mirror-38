from functools import partial

import graphene
from django.core.paginator import Paginator
from graphene_django.utils import maybe_queryset


class ModelField(graphene.Field):
    """
    Adds id and slug to the filter fields.  # todo: implement slug with natural key lookup

    .. code:
       class Query(graphene.ObjectType):
           user = ModelField(UserType)

    """

    def __init__(self, _type, id=graphene.Int(required=True), *args, **kwargs):
        kwargs.update(id=id, )
        super(ModelField, self).__init__(_type, *args, **kwargs)

    @classmethod
    def model_resolver(cls, resolver, _type, root, info,
                       id: int = None,
                       # slug: str = None,
                       **args):
        # todo: add call to a get_queryset function/partial
        # print('  ', resolver(root, info))
        return _type._meta.model.objects.get(id=id)  # todo: don't use objects?

    def get_resolver(self, parent_resolver):
        print('PARENT', parent_resolver)
        return partial(self.model_resolver, parent_resolver, self._type)


class PaginatorField(graphene.Field):
    def __init__(self, _type,
                 per_page=graphene.Int(default_value=100),
                 orphans=graphene.Int(default_value=0),
                 # allow_empty_first_page  # todo: from paginator?
                 page=graphene.Int(default_value=1),
                 *args, **kwargs):
        kwargs.update(per_page=per_page,
                      orphans=orphans,
                      page=page)

        assert getattr(_type._meta, 'paginator', False), '{} needs to have a paginator.'.format(_type)
        self._type = _type._meta.paginator

        super(PaginatorField, self).__init__(self._type, *args, **kwargs)

    @classmethod  # never called
    def __init_subclass_with_meta__(cls, **kwargs):
        print('PageList', '__init_subclass_with_meta__', kwargs)
        super(PaginatorField, cls).__init_subclass_with_meta__(**kwargs)

    # @property
    # def type(self):
    #     return get_type(self._type)

    @classmethod
    def page_resolver(cls, resolver, _type, root, info,
                      per_page: int = None,
                      page: int = None,
                      orphans: int = None,
                      **args):
        # per_page = args.pop('per_page')
        pager_ret = resolver(root, info, **args)
        paginator = Paginator(maybe_queryset(pager_ret), per_page=per_page, orphans=orphans)
        page = paginator.page(page)
        # _type = cls.type
        return _type(object_count=paginator.count,
                     num_pages=paginator.num_pages,
                     # page_range = graphene.List()
                     has_next_page=page.has_next(),
                     has_previous_page=page.has_previous(),
                     has_other_pages=page.has_other_pages(),
                     # next_page_number=page.next_page_number(),  # todo: catch error
                     # previous_page_number=page.previous_page_number(),  # todo: catch error
                     start_index=page.start_index(),
                     end_index=page.end_index(),
                     object_list=page.object_list,
                     )
        # return Paginator(num_pages=1)

    def get_resolver(self, parent_resolver):
        return partial(self.page_resolver, parent_resolver, self._type)


class FilterField(graphene.Field):
    pass


class PaginatorFilterField(graphene.Field):
    pass
