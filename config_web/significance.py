from biothings.web.settings.default import APP_LIST
# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = 'outbreak-significance'
API_PREFIX = 'significance'
API_VERSION = ''

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.GRMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.GRQueryHandler"),
]

