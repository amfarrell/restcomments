import traceback
import sys
import logging

logger = logging.getLogger('django')

class ProcessExceptionMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 200:
            logger.error('\n'.join(traceback.format_exception(*sys.exc_info())))
        return response
