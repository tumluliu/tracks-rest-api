#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RESTful API of GPS tracks information
"""

import os
import sys
import logging.config
import json

LOGGING_CONF_FILE = 'logging.json'
DEFAULT_LOGGING_LVL = logging.INFO
path = LOGGING_CONF_FILE
value = os.getenv('LOG_CFG', None)
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask
from flask_cors import CORS
from tracksdb import Session, Track, TrackInfo, \
    track_serializer, trackinfo_serializer
import flask_restless

app = Flask(__name__)
cors = CORS(app)
manager = flask_restless.APIManager(app, session=Session)

track_blueprint = manager.create_api(
    Track,
    methods=['GET'],
    results_per_page=10,
    max_results_per_page=50,
    serializer=track_serializer)
trackinfo_blueprint = manager.create_api(
    TrackInfo,
    methods=['GET'],
    results_per_page=10,
    max_results_per_page=50,
    serializer=trackinfo_serializer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
