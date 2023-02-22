import biothings.hub.databuild.builder as builder

from hub.databuild.mapper import DateMapper

class ResourcesBuilder(builder.DataBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mappers = {None: DateMapper(name="resources")}
