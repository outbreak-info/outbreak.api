# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-significance"
API_PREFIX = "significance"
ES_DOC_TYPE = "significance"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.GRMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.GRQueryHandler"),
]
