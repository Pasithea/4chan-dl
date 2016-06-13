import logging
import sys

logger = logging.getLogger('chan')
logger.setLevel(logging.DEBUG)
stdouthandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
stdouthandler.setFormatter(formatter)
logger.addHandler(stdouthandler)
