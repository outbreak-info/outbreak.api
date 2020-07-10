from biothings.web.handlers import BiothingHandler, QueryHandler


class OutbreakBiothingHandler(BiothingHandler):

    name = 'typed_annotation'


class OutbreakQueryHandler(QueryHandler):

    name = 'typed_query'
