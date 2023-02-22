#!/usr/bin/env python
import logging
import os

from functools import partial
import biothings
from biothings.utils.version import set_versions

import config

logging.getLogger("requests").setLevel(logging.ERROR)

app_folder, _src = os.path.split(os.path.split(os.path.abspath(__file__))[0])
set_versions(config, app_folder)

from biothings.hub import HubServer

import hub.dataload.sources


#outbreak_features =  getattr(config, "HUB_FEATURES", None)

class OutBreakHubServer(HubServer):
    #DEFAULT_FEATURES = config.HUB_FEATURES

    def configure_build_manager(self):
        # set specific managers
        import biothings.hub.databuild.builder as builder
        from hub.databuild.builder import ResourcesBuilder
        build_manager = builder.BuilderManager(builder_class=ResourcesBuilder,job_manager=self.managers["job_manager"])
        build_manager.configure()
        build_manager.poll()
        self.managers["build_manager"] = build_manager


server = OutBreakHubServer(hub.dataload.sources, name=config.HUB_NAME)


if __name__ == "__main__":
    config.logger.info("Hub DB backend: %s", biothings.config.HUB_DB_BACKEND)
    config.logger.info("Hub database: %s", biothings.config.DATA_HUB_DB_DATABASE)
    server.start()
