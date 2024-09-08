import logging


def logger_setup(module):
  
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler = logging.StreamHandler()
  handler.setFormatter(formatter)
  
  custom_logger = logging.getLogger(__name__)
  custom_logger.setLevel(logging.DEBUG)
  custom_logger.addHandler(handler)
  return custom_logger