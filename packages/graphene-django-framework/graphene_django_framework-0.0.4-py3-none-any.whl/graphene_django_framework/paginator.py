import graphene


class PageType(graphene.ObjectType):
    def __init__(self, *args, **kwargs):
        super(PageType, self).__init__(*args, **kwargs)

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
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
        description = 'This is a Paginator'  # todo: remove
