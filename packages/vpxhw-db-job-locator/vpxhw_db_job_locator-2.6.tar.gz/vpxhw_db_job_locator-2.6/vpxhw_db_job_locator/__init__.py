import logging

# create vpx_logger
vpx_logger = logging.getLogger(__name__)
# vpx_logger.setLevel(logging.DEBUG)
vpx_logger.setLevel(logging.WARNING)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    "%(process)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to vpx_logger
vpx_logger.addHandler(ch)

vpx_logger.debug("starting vpx logger")
vpx_logger.info("starting vpx logger")
