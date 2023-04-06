from biothings.web.settings.default import APP_LIST
# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_HOST = 'su11:9200'
ES_INDEX = 'significance_202303311627_cmcubndw'
API_PREFIX = 'significance'
API_VERSION = ''

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.GRMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.GRQueryHandler"),
]

