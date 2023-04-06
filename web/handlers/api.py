from biothings.web.handlers import BiothingHandler, QueryHandler, MetadataSourceHandler
from .genomics.gisaid_auth import gisaid_authorized


# *****************************************************************************
# Resource Handlers
# *****************************************************************************
class OutbreakBiothingHandler(BiothingHandler):

    name = 'typed_annotation'


class OutbreakQueryHandler(QueryHandler):

    name = 'typed_query'

# *****************************************************************************
# Significance Handlers
# *****************************************************************************

class GRQueryHandler(QueryHandler):
    @gisaid_authorized
    async def get(self, *args, **kwargs):
        await super().get(*args, **kwargs)

class GRMetadataSourceHandler(MetadataSourceHandler):
    @gisaid_authorized
    async def get(self, *args, **kwargs):
        await super().get(*args, **kwargs)
