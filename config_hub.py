# ######### #
# HUB VARS  #
# ######### #
import os
import logging

from biothings.utils.configuration import ConfigurationError

DATA_HUB_DB_DATABASE = "biothings_hubdb"   # db containing the following (internal use)
DATA_SRC_MASTER_COLLECTION = 'src_master'  # for metadata of each src collections
DATA_SRC_DUMP_COLLECTION = 'src_dump'      # for src data download information
DATA_SRC_BUILD_COLLECTION = 'src_build'    # for src data build information
DATA_SRC_BUILD_CONFIG_COLLECTION = 'src_build_config'
DATA_PLUGIN_COLLECTION = 'data_plugin'     # for data plugins information
API_COLLECTION = 'api'                     # for api information (running under hub control)
CMD_COLLECTION = 'cmd'                     # for cmd launched from the hub
EVENT_COLLECTION = 'event'                 # for event propagation

# Redis config to cache IDs when doing cold/hot merge
REDIS_CONNECTION_PARAMS = {}

# where to store info about processes launched by the hub
RUN_DIR = '/tmp/run'

# reporting diff results, number of IDs to consider (to avoid too much mem usage)
MAX_REPORTED_IDS = 1000
# for diff updates, number of IDs randomly picked as examples when rendering the report
MAX_RANDOMLY_PICKED = 10
# size in bytes for a diff file (used in diff/reduce step)
MAX_DIFF_SIZE = 10 * 1024**2

# ES s3 repository to use snapshot/restore (must be pre-configured in ES)
SNAPSHOT_REPOSITORY = "outbreak_repository"

# cache file format ("": ascii/text uncompressed, or "gz|zip|xz"
CACHE_FORMAT = "xz"

# How much memory hub is allowed to use:
# - "auto", let hub decides (will use 50%-60% of available RAM)
# - None: no limit
# - otherwise specify a number in bytes
HUB_MAX_MEM_USAGE = None

# Max number of *processes* hub can access to run jobs
HUB_MAX_WORKERS = max(1, int(os.cpu_count() / 4))
# Max number of *threads* hub can use (will default to HUB_MAX_WORKERS if undefined)
HUB_MAX_THREADS = HUB_MAX_WORKERS
MAX_SYNC_WORKERS = HUB_MAX_WORKERS

# Max queued jobs in job manager
# this shouldn't be 0 to make sure a job is pending and ready to be processed
# at any time (avoiding job submission preparation) but also not a huge number
# as any pending job will consume some memory).
MAX_QUEUED_JOBS = os.cpu_count() * 4

# when creating a snapshot, how long should we wait before querying ES
# to check snapshot status/completion ? (in seconds)
# Since myvariant's indices are pretty big, a whole snaphost won't happen in few secs,
# let's just monitor the status every 5min
MONITOR_SNAPSHOT_DELAY = 5 * 60

# Hub environment (like, prod, dev, ...)
# Used to generate remote metadata file, like "latest.json", "versions.json"
# If non-empty, this constant will be used to generate those url, as a prefix
# with "-" between. So, if "dev", we'll have "dev-latest.json", etc...
# "" means production
HUB_ENV = ""

# Pre-prod/test ES definitions
INDEX_CONFIG = {
    #"build_config_key" : None, # used to select proper idxr/syncer
    "indexer_select": {
        # default
        None : "path.to.special.Indexer",
    },
    "env" : {
        "test": {
            "host": "localhost:9200",
            "indexer": {
                "args": {
                    "timeout": 300,
                    "retry_on_timeout": True,
                    "max_retries": 10,
                    },
                },
            "index": [],
        }
    },
}

# Snapshot environment configuration
SNAPSHOT_CONFIG = {}
RELEASE_CONFIG = {}

# SSH port for hub console
HUB_SSH_PORT = 19122
HUB_API_PORT = 19180
READONLY_HUB_API_PORT = 19181

# Hub name/icon url/version, for display purpose
HUB_NAME = "OutBreak API (backend)"
HUB_ICON = "https://outbreak.info/img/icon-01.1a356632.svg"
HUB_VERSION = "master"

USE_RELOADER = True # so no need to restart hub when a datasource has changed

################################################################################
# HUB_PASSWD
################################################################################
# The format is a dictionary of 'username': 'cryptedpassword'
# Generate crypted passwords with 'openssl passwd -crypt'
# The default value below is for an empty password
HUB_PASSWD = {"guest":"9RKfd8gDuNf0Q"}

# cached data (it None, caches won't be used at all)
CACHE_FOLDER = None

STANDALONE_AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
}

STANDALONE_CONFIG = { 
    # default config
    "_default": {
        "es_host" : "localhost:9200",
        "index" : "outbreak-covid19-dev",
        }, 
    "outbreak-covid19" : {
        "es_host": "prodserver:9200",
        "index": "outbreak-covid19",
        }
}

#AUTOHUB_INDEXER_FACTORY = "biothings.hub.dataindex.indexer.DynamicIndexerFactory"
#AUTOHUB_ES_HOST = "localhost:9200"


from biothings.utils.loggers import setup_default_log

########################################
# APP-SPECIFIC CONFIGURATION VARIABLES #
########################################
# The following variables should or must be defined in your
# own application. Create a config.py file, import that config_common
# file as:
#
#   from config_hub import *
#
# then define the following variables to fit your needs. You can also override any
# any other variables in this file as required. Variables defined as ValueError() exceptions
# *must* be defined
#


# Individual source database connection
DATA_SRC_SERVER = ConfigurationError("Define hostname for source database")
DATA_SRC_PORT = ConfigurationError("Define port for source database")
DATA_SRC_DATABASE = ConfigurationError("Define name for source database")
DATA_SRC_SERVER_USERNAME = ConfigurationError("Define username for source database connection (or None if not needed)")
DATA_SRC_SERVER_PASSWORD = ConfigurationError("Define password for source database connection (or None if not needed)")

# Target (merged collection) database connection
DATA_TARGET_SERVER = ConfigurationError("Define hostname for target database (merged collections)")
DATA_TARGET_PORT = ConfigurationError("Define port for target database (merged collections)")
DATA_TARGET_DATABASE = ConfigurationError("Define name for target database (merged collections)")
DATA_TARGET_SERVER_USERNAME = ConfigurationError("Define username for target database connection (or None if not needed)")
DATA_TARGET_SERVER_PASSWORD = ConfigurationError("Define password for target database connection (or None if not needed)")

HUB_DB_BACKEND = ConfigurationError("Define Hub DB connection")
# Internal backend. Default to mongodb
# For now, other options are: mongodb, sqlite3, elasticsearch
#HUB_DB_BACKEND = {
#        "module" : "biothings.utils.sqlite3",
#        "sqlite_db_foder" : "./db",
#        }
#HUB_DB_BACKEND = {
#        "module" : "biothings.utils.mongo",
#        "uri" : "mongodb://localhost:27017",
#        #"uri" : "mongodb://user:passwd@localhost:27017", # mongodb std URI
#        }
#HUB_DB_BACKEND = {
#        "module" : "biothings.utils.es",
#        "host" : "localhost:9200",
#        }

#ES_HOST = ConfigurationError("Define ElasticSearch host used for index creation (eg localhost:9200)")

# S3 bucket, root of all biothings releases information
S3_RELEASE_BUCKET = "biothings-releases"
# bucket/folder containing releases
S3_DIFF_BUCKET = "biothings-diffs"
# what sub-folder should be used within diff bucket to upload diff files
S3_APP_FOLDER = "pending" # actual pending datasource name will be appended


TORNADO_SETTINGS = {
    # max 10GiB upload
    "max_buffer_size" : 10*1024*1024*1024,
}

STANDALONE_VERSION = {"branch" : "standalone_v3"}

# Path to a folder to store all downloaded files, logs, caches, etc...
DATA_ARCHIVE_ROOT = ConfigurationError("Define path to folder which will contain all downloaded data, cache files, etc...")

# Path to a folder to store all 3rd party parsers, dumpers, etc...
DATA_PLUGIN_FOLDER = ConfigurationError("Define path to folder which will contain all 3rd party parsers, dumpers, etc...")

DATA_UPLOAD_FOLDER = ConfigurationError("Define path to folder where uploads to API are stored")

# Path to folder containing diff files
DIFF_PATH = ConfigurationError("Define path to folder which will contain output files from diff")
# Usually inside DATA_ARCHIVE_ROOT
#DIFF_PATH = os.path.join(DATA_ARCHIVE_ROOT,"diff")

# Path to folder containing release note files
RELEASE_PATH = ConfigurationError("Define path to folder which will contain release files")
# Usually inside DATA_ARCHIVE_ROOT
#RELEASE_PATH = os.path.join(DATA_ARCHIVE_ROOT,"release")

# this dir must be created manually
LOG_FOLDER = ConfigurationError("Define path to folder which will contain log files")
# Usually inside DATA_ARCHIVE_ROOT
#LOG_FOLDER = os.path.join(DATA_ARCHIVE_ROOT,'logs')

# When ES repository type is "fs", where snapshot should be stored
ES_BACKUPS_FOLDER = ConfigurationError("Define path to folder which will contain ES snapshot when type='fs'")

# List of versions.json URLs, Hub will handle these as sources for data releases
VERSION_URLS = []

# default hub logger
logger = ConfigurationError("Provider a default hub logger instance (use setup_default_log(name,log_folder)")
# Usually use default setup
#logger = setup_default_log("hub", LOG_FOLDER)

