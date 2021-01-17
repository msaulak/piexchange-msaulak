"""Module to represent the constituents of an outgoing email"""
from typing import Dict, Any

from src.utils.helper_methods import object_to_str, log_and_call


class OutgoingEmail:
    """Class to encapsulate the fields and constituents of an outgoing email."""
    def __init__(self, **outgoing_email_dict):
        self.sender: str = outgoing_email_dict['sender'] # from is a keyword in py, hence using sender
        self.to: str = outgoing_email_dict['to']
        self.subject: str = outgoing_email_dict['subject']
        self.mime_type: str = outgoing_email_dict['mime_type']
        self.body: str = outgoing_email_dict['body']

    def __repr__(self):
        return object_to_str(self)

    def __str__(self):
        return object_to_str(self)

    @log_and_call
    def to_serializable_json(self) -> Dict[str, Any]:
        """Returns a dict representation of the instance. Can be used for
        serialization. Did not use __dict__ as it return methods as well.
        Returns:
            dict: dictionary representation of serializable fields
        """
        return {
            'from': self.sender,
            'to': self.to,
            'subject': self.subject,
            'mimeType': self.mime_type,
            'body': self.body
        }