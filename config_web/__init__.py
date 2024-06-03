from . import covid19, genomics, growth_rate, resources, significance, wastewater, wastewater_demix, wastewater_demix_weekly, wastewater_metadata, wastewater_variants

try:
    from config_web_local import *
except ImportError:
    pass
