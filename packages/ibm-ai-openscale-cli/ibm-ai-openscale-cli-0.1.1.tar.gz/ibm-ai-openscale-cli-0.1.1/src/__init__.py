# coding=utf-8
from __future__ import print_function
import logging

# Colors
logging.addLevelName( logging.WARNING, "\033[1;93m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(name)-12s %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(ch)

# Disable AIOS warnings
logging.getLogger('handle_response').setLevel(logging.WARNING)
logging.getLogger('ibm_ai_openscale.utils.client_errors').setLevel(logging.WARNING)
name = 'ibm-ai-openscale-cli'
