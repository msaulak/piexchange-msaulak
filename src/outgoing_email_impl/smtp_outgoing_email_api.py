import logging

from src.lib.outgoing_email import OutgoingEmail
from src.lib.outgoing_email_api import OutgoingEmailApi
from src.utils.helper_methods import log_and_call

logger = logging.getLogger('pi.exchange.emailsender')


class SMTPOutgoingEmailApi(OutgoingEmailApi):
    def __init__(self):
        super(SMTPOutgoingEmailApi, self).__init__()

    @log_and_call
    def send_message(self, outgoing_email: OutgoingEmail):
        logger.info(f'Implement this class to send outgoing via SMTP.')
