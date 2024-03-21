# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-wastewater-demix"
API_PREFIX = "wastewater_demix"
ES_DOC_TYPE = "wastewater_demix"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.GRMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.GRQueryHandler"),
]
