from copy import deepcopy

from biothings.web.settings.default import (ANNOTATION_KWARGS, APP_LIST,
                                            QUERY_KWARGS)

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
# ES_HOST = 'localhost:9200'
ES_INDEX = 'outbreak-resources-*'
ES_DOC_TYPE = 'resource'

# *****************************************************************************
# Web Application
# *****************************************************************************
API_PREFIX = 'resources'
API_VERSION = ''
APP_LIST = deepcopy(APP_LIST)
APP_LIST += [
    (r"/{pre}/{ver}/([^\/]+)/query/?", 'web.handlers.OutbreakQueryHandler'),
    (r"/{pre}/{ver}/([^\/]+)/([^\/]+)/?", 'web.handlers.OutbreakBiothingHandler'),
    (r"/{pre}/{ver}/([^\/]+)/?", 'web.handlers.OutbreakBiothingHandler')
]

# *****************************************************************************
# Query Pipeline
# *****************************************************************************
ES_QUERY_BUILDER = 'web.pipeline.QueryBuilder'
ALLOW_NESTED_AGGS = True

# *****************************************************************************
# Endpoint Specifics
# *****************************************************************************
ANNOTATION_DEFAULT_SCOPES = ['_id', '@id']
ANNOTATION_KWARGS = deepcopy(ANNOTATION_KWARGS)
ANNOTATION_KWARGS['*']['always_list']['default'] = ['creator.affiliation']
QUERY_KWARGS = deepcopy(QUERY_KWARGS)
QUERY_KWARGS['*']['always_list']['default'] = ['creator.affiliation']
TYPED_ANNOTATION_KWARGS = deepcopy(ANNOTATION_KWARGS)
TYPED_ANNOTATION_KWARGS['*']['_type'] = {'type': str, 'path': 0, 'group': 'esqb'}
TYPED_ANNOTATION_KWARGS['GET']['id']['path'] = 1
TYPED_QUERY_KWARGS = deepcopy(QUERY_KWARGS)
TYPED_QUERY_KWARGS['*']['_type'] = {'type': str, 'path': 0, 'group': 'esqb'}
