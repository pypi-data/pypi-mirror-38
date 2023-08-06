from functools import partial
import graphene

from graphene_django.utils import maybe_queryset
from django.core.paginator import Paginator


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
        # print('PageList', '__init_subclass_with_meta__', kwargs)
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
        print('Paginator', root, info, args)
        # print("  field_name",info.field_name,)
        # print("  field_asts",info.field_asts,)
        # print("  return_type",info.return_type,)
        print("  parent_type",info.parent_type,)
        # print("  schema",info.schema,)
        # print("  fragments",info.fragments,)
        print("  root_value",info.root_value,)
        # print("  operation",info.operation,)
        # print("  variable_values",info.variable_values,)
        # print("  context",info.context,)
        # print("  path",info.path,)
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
        print('Paginator', 'get_resolver', self._type, parent_resolver)
        return partial(self.page_resolver, parent_resolver, self._type)

    # def get_resolver(self, parent_resolver):
    #     print('PageList', 'get_resolver', self.resolver)
    #     print('PageList', 'get_resolver', parent_resolver)
    #     return partial()


class FilterField(graphene.Field):
    pass


class PaginatorFilterField(graphene.Field):
    pass
