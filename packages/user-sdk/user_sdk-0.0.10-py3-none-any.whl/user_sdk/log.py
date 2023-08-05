import logging
import json


logger = logging.getLogger(__name__)

def log(message: str, request_url: str, status_code: str,
        response: dict, request_body: dict = None):

    dict = {
            'request_url': request_url,
            'request_body': request_body,
            'status_code': status_code,
            'response': json.dumps(response)
        }
    logger.error('%s' % message, extra=dict)
