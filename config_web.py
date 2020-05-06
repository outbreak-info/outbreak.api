# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_HOST = 'localhost:9200'
ES_INDEX = 'zenodo_covid,outbreak-litcovid'
ES_DOC_TYPE = 'zenodo'
ES_INDICES = {
    "covid19":"outbreak-covid19",
    "litcovid": "outbreak-litcovid",
    "zenodo":"zenodo_covid",
}

# *****************************************************************************
# Web Application
# *****************************************************************************

API_PREFIX = 'resources'
API_VERSION = ''

# *****************************************************************************
# Analytical Statistics
# *****************************************************************************

GA_ACTION_QUERY_GET = 'query_get'
GA_ACTION_QUERY_POST = 'query_post'
GA_ACTION_ANNOTATION_GET = 'outbreak_get'
GA_ACTION_ANNOTATION_POST = 'outbreak_post'
GA_TRACKER_URL = 'api.outbreak.info'

# *****************************************************************************
# Endpoint Specifics
# *****************************************************************************

STATUS_CHECK = {
    'id': 'USA_US-CA_06073_2020-03-01',  # San Diego County
    'index': 'outbreak-covid19',
    'doc_type': 'outbreak_info'
}

try:
    from config_web_local import *
except ImportError:
    pass
