# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_INDEX = "outbreak-wastewater-demix-weekly"
API_PREFIX = "wastewater_demix_weekly"
ES_DOC_TYPE = "wastewater_demix_weekly"
API_VERSION = ""

APP_LIST = [
    (r"/{pre}/{ver}/metadata/?", "web.handlers.WWMetadataSourceHandler"),
    (r"/{pre}/{ver}/query/?", "web.handlers.WWQueryHandler"),
]
