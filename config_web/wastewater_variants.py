# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-wastewater-variants"
API_PREFIX = "wastewater_variants"
ES_DOC_TYPE = "wastewater_variants"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.WWMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.WWQueryHandler"),
]
