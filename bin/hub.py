#!/usr/bin/env python
import os
import config
import biothings
from biothings.utils.version import set_versions

app_folder, _src = os.path.split(os.path.split(os.path.abspath(__file__))[0])
set_versions(config, app_folder)
biothings.config_for_app(config)
logging = config.logger


from biothings.hub import HubServer
import hub.dataload.sources


if getattr(config, "HUB_FEATURES", None):
    class OutBreakHubServer(HubServer):
        DEFAULT_FEATURES = config.HUB_FEATURES
    server = OutBreakHubServer(hub.dataload.sources, name=config.HUB_NAME)
else:
    server = HubServer(hub.dataload.sources, name=config.HUB_NAME)


if __name__ == "__main__":
    logging.info("Hub DB backend: %s", biothings.config.HUB_DB_BACKEND)
    logging.info("Hub database: %s", biothings.config.DATA_HUB_DB_DATABASE)
    server.start()
