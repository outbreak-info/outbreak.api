from copy import deepcopy

from biothings.web.settings.default import ANNOTATION_KWARGS, QUERY_KWARGS

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_HOST = 'localhost:9200'
ES_INDEX = 'outbreak-resources-*'
ES_DOC_TYPE = 'resource'
ES_INDICES = {
    "publication":"outbreak-resources-publication",
    "clinicaltrial": "outbreak-resources-clinicaltrial",
    "dataset":"outbreak-resources-dataset",
}

# *****************************************************************************
# Web Application
# *****************************************************************************
API_PREFIX = 'resources'
API_VERSION = ''

# *****************************************************************************
# Query Pipeline
# *****************************************************************************
ES_RESULT_TRANSFORM = 'web.pipeline.ResourceTransform'
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
