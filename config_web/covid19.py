from copy import deepcopy

from biothings.web.settings.default import ANNOTATION_KWARGS, QUERY_KWARGS

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
ES_HOST = 'localhost:9200'
ES_INDEX = 'outbreak-covid19'
ES_DOC_TYPE = 'outbreak_info'

# *****************************************************************************
# Web Application
# *****************************************************************************

API_PREFIX = 'covid19'
API_VERSION = ''

# *****************************************************************************
# Endpoint Specifics
# *****************************************************************************

# TODO Remove after biothings update

ANNOTATION_KWARGS = deepcopy(ANNOTATION_KWARGS)
ANNOTATION_KWARGS['*']['_sorted']['default'] = False

QUERY_KWARGS = deepcopy(QUERY_KWARGS)
QUERY_KWARGS['*']['_sorted']['default'] = False

#------------------------------------

STATUS_CHECK = {
    'id': 'USA_US-CA_06073_2020-03-01',  # San Diego County
    'index': 'outbreak-covid19',
    'doc_type': 'outbreak_info'
}
