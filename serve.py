#!/usr/bin/python3

import spendendings
from waitress import serve
from paste.translogger import TransLogger
import sys

port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])

serve(TransLogger(spendendings.create_app({
    'SHOW_PROJECT_INDEX': True
})), port=port)
