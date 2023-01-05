from .lineage import LineageMutationsHandler
# from .prevalence import PrevalenceByLocationAndTimeHandler

routes = [
    (r"/v2/genomics/lineage-mutations", LineageMutationsHandler),
    # (r"/v2/genomics/prevalence-by-location", PrevalenceByLocationAndTimeHandler),
]
