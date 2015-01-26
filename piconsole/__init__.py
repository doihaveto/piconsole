import logging.config
from . import settings
from flask import Flask

logging.config.dictConfig(settings.LOGGING)
app = Flask(__name__)

import baseconsole
