from copy import deepcopy

from biothings.web.settings.default import ANNOTATION_KWARGS, QUERY_KWARGS

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_HOST = 'localhost:9200'
ES_INDEX = 'all-resources'
ES_DOC_TYPE = '_all'
ES_INDICES = {
    "zenodo":"zenodo_covid",
    "litcovid": "outbreak-litcovid",
    "biorxiv":"outbreak-biorxiv",
    "clinical_trials":"outbreak-clinical_trials",
}

# *****************************************************************************
# Web Application
# *****************************************************************************
API_PREFIX = 'resources'
API_VERSION = ''

# *****************************************************************************
# Web Application
# *****************************************************************************
ES_RESULT_TRANSFORM = 'web.pipeline.ResourceTransform'

# *****************************************************************************
# Endpoint Specifics
# *****************************************************************************
ANNOTATION_DEFAULT_SCOPES = ['_id', '@id']
ANNOTATION_KWARGS = deepcopy(ANNOTATION_KWARGS)
ANNOTATION_KWARGS['*']['always_list']['default'] = ['creator.affiliation']
QUERY_KWARGS = deepcopy(QUERY_KWARGS)
QUERY_KWARGS['*']['always_list']['default'] = ['creator.affiliation']
