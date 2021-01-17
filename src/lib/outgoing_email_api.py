"""Abstract class for an API which can be used to send outgoing emails"""
from src.lib.outgoing_email import OutgoingEmail


class OutgoingEmailApi:
    """Abstract class which can be implemented for sending out emails
    """
    def __init__(self):
        pass

    def send_message(self, outgoing_email: OutgoingEmail) -> NotImplementedError:
        """
        Override this method in inheritor for outgoing email functionaloty
        Args:
            outgoing_email (OutgoingEmail): instance of OutgoingEmail which needs to be sent out.

        Raises NotImplementedError

        """
        raise NotImplementedError(f'send_message must be implemented')
