from . import covid19, genomics, growth_rate, resources, significance, wastewater

try:
    from config_web_local import *
except ImportError:
    pass
