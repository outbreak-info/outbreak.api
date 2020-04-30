#!/usr/bin/env python
import logging


import biothings
import config
from biothings.utils.version import set_versions
# from standalone.utils.version import set_standalone_version

# shut some mouths...
logging.getLogger("elasticsearch").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("tornado").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)

# fill app & autohub versions
set_versions(config, ".")
# set_standalone_version(config, "standalone")
biothings.config_for_app(config)
# now use biothings' config wrapper
config = biothings.config
logging.info("Hub DB backend: %s", config.HUB_DB_BACKEND)
logging.info("Hub database: %s", config.DATA_HUB_DB_DATABASE)

from biothings.hub.dataindex.indexer import DynamicIndexerFactory
from biothings.hub.standalone import AutoHubServer 


class OutBreakHubServer(AutoHubServer):
    DEFAULT_FEATURES = AutoHubServer.DEFAULT_FEATURES + ["index", "api"]


server = OutBreakHubServer(source_list=None, name="Outbreak API Hub (frontend)",
    api_config=None, dataupload_config=False, websocket_config=False
)


if __name__ == "__main__":
    server.start()
