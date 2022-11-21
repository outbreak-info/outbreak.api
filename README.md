# outbreak.api
The data API server for outbreak.info

[![DOI](https://zenodo.org/badge/248579616.svg)](https://zenodo.org/badge/latestdoi/248579616)

##  To install dependecies

  (recommend to setup a fresh Python venv first)

    pip install -r requirements_web.txt
    pip install -r requirements_hub.txt

## To start the dev server

  (require to have ES running at `localhost:9200` by default)

    python index.py --debug --conf=config_web

  To override the default settings, create a `config_web_local.py` on the root folder and include extra settings.
