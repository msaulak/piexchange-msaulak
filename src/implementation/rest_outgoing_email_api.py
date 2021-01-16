import logging

from src.lib.outgoing_email import OutgoingEmail
from src.lib.outgoing_email_api import OutgoingEmailApi

logger = logging.getLogger('pi.exchange.emailsender')

class RESTOutgoingEmailApi(OutgoingEmailApi):
    def __init__(self):
        super(RESTOutgoingEmailApi, self).__init__()

    def send_message(self, outgoing_email: OutgoingEmail):
        logger.info(f'Implement this class to send outgoing {outgoing_email} via a REST API.')