from . import covid19
from . import resources

try:
    from config_web_local import *
except ImportError:
    pass

# *****************************************************************************
# Analytical Statistics
# *****************************************************************************

GA_ACTION_QUERY_GET = 'query_get'
GA_ACTION_QUERY_POST = 'query_post'
GA_ACTION_ANNOTATION_GET = 'outbreak_get'
GA_ACTION_ANNOTATION_POST = 'outbreak_post'
GA_TRACKER_URL = 'api.outbreak.info'
