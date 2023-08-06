import functools
import threading
import logging
import logging.config

from flask_log_request_id import RequestID, RequestIDLogFilter

class RequestIdLogger():

    __logger = None

    @staticmethod
    def getLogger(app):
        if RequestIdLogger.__logger == None:
            RequestIdLogger(app)
        return RequestIdLogger.__logger

    def __init__(self, app):
        RequestID(app)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(request_id)s - %(funcName)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.addFilter(RequestIDLogFilter())
        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        RequestIdLogger.__logger = logger
        

def getLogger(app):
    if app == None:
        raise Exception("Please provide a flask app instance.")
    return RequestIdLogger.getLogger(app)
