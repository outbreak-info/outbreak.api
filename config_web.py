# from biothings.web.settings.default import *

# from web.api.query_builder import ESQueryBuilder
# from web.api.query import ESQuery
# from web.api.transform import ESResultTransformer

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
# elasticsearch server transport url
ES_HOST = 'localhost:9200'
# elasticsearch index name
ES_INDEX = 'outbreak-covid19'
# elasticsearch document type
ES_DOC_TYPE = 'outbreak_info'
# make these smaller for c.biothings
#ES_SIZE_CAP = 10
# scrolls are smaller
#ES_SCROLL_SIZE = 10
ES_SCROLL_TIME = '10m'

API_VERSION = 'v1'

# *****************************************************************************
# App URL Patterns
# *****************************************************************************
#APP_LIST = [
#    (r"/{}/status".format(API_VERSION), StatusHandler),
#    (r"/{}/outbreak_info/(.+)/?".format(API_VERSION), BiothingHandler),
#    (r"/{}/outbreak_info/?$".format(API_VERSION), BiothingHandler),
#    (r"/{}/query/?".format(API_VERSION), QueryHandler),
#    (r"/{}/metadata/?".format(API_VERSION), MetadataSourceHandler),
#    (r"/{}/metadata/fields/?".format(API_VERSION), MetadataFieldHandler),
#
#    (r"/?", MainHandler),
#    (r"/([^/]+)/?", ApiViewHandler)
#]

###############################################################################
#   app-specific query builder, query, and result transformer classes
###############################################################################

# *****************************************************************************
# Subclass of biothings.web.api.es.query_builder.ESQueryBuilder to build
# queries for this app
# *****************************************************************************
# ES_QUERY_BUILDER = ESQueryBuilder
# *****************************************************************************
# Subclass of biothings.web.api.es.query.ESQuery to execute queries for this app
# *****************************************************************************
# ES_QUERY = ESQuery
# *****************************************************************************
# Subclass of biothings.web.api.es.transform.ESResultTransformer to transform
# ES results for this app
# *****************************************************************************
# ES_RESULT_TRANSFORMER = ESResultTransformer

GA_ACTION_QUERY_GET = 'query_get'
GA_ACTION_QUERY_POST = 'query_post'
GA_ACTION_ANNOTATION_GET = 'outbreak_get'
GA_ACTION_ANNOTATION_POST = 'outbreak_post'
GA_TRACKER_URL = 'api.outbreak.info'

# ANNOTATION_ID_REGEX_LIST = []

# make max sizes smaller
#QUERY_GET_ES_KWARGS['size']['default'] = 10
#ANNOTATION_POST_CONTROL_KWARGS['ids']['max'] = 10
#QUERY_POST_CONTROL_KWARGS['q']['max'] = 10

STATUS_CHECK = {
    'id': 'USA_US-CA_06073_2020-03-01',  # San Diego County
    'index': 'outbreak-covid19',
    'doc_type': 'outbreak_info'
}

STATIC_PATH = 'web/static'

# JSONLD_CONTEXT_PATH = 'web/context/context.json'

try:
    from config_web_local import *
except ImportError:
    pass
