# ######### #
# HUB VARS  #
# ######### #

# ES s3 repository to use snapshot/restore (must be pre-configured in ES)
SNAPSHOT_REPOSITORY = "outbreak_repository"

# Pre-prod/test ES definitions
INDEX_CONFIG = {
    #"build_config_key" : None, # used to select proper idxr/syncer
    "indexer_select": {
        # default
        #None : "path.to.special.Indexer",
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
HUB_ICON = "https://outbreak.info/assets/icon-01-d7c2932d.svg"
HUB_VERSION = "master"

USE_RELOADER = False

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

# List of versions.json URLs, Hub will handle these as sources for data releases
VERSION_URLS = []
