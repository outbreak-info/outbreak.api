from . import covid19, genomics, growth_rate, resources, significance

try:
    from config_web_local import *
except ImportError:
    pass
