# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-wastewater"
API_PREFIX = "wastewater"
ES_DOC_TYPE = "wastewater"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.WWMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.WWQueryHandler"),
]
