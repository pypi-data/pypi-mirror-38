import graphene


class PageType(graphene.ObjectType):
    def __init__(self, *args, **kwargs):
        # print('PageType', '__init__', args, kwargs)
        super(PageType, self).__init__(*args, **kwargs)

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        # print('PageType', 'options', options)
        super(PageType, cls).__init_subclass_with_meta__(**options)


class Paginator(PageType):
    object_count = graphene.Int()  # conflicts with count attr
    num_pages = graphene.Int(abs=graphene.Boolean(default_value=False))
    # page_range = graphene.List()  # todo: implement this
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    has_other_pages = graphene.Boolean()
    next_page_number = graphene.Int()
    previous_page_number = graphene.Int()
    start_index = graphene.Int()
    end_index = graphene.Int()

    # object_list = graphene.List(UserType)  # dynamically created with PageList

    class Meta:
        description = 'This is a Paginator'

    # @classmethod
    # def __init_subclass_with_meta__(cls, **options):
    #     print('Paginator', 'options', options)
    #     super(Paginator, cls).__init_subclass_with_meta__(**options)

    # def resolve_num_pages(self, info, abs=None, **kwargs):
    #     return 1 if abs else -1

    # def resolve_object_list(self, info, **kwargs):
    #     print('resolve_object_list', kwargs)
    #     print('Paginator', 'resolve_object_list', info)
    #     return [UserType(**{'username': 'PAGE ONE', 'first_name': 'FIRST PAGE', 'last_name': 'LAGE PAGE'}), ]
