# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-wastewater-metadata"
API_PREFIX = "wastewater_metadata"
ES_DOC_TYPE = "wastewater_metadata"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.GRMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.GRQueryHandler"),
]
