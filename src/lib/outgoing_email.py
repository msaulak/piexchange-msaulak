from src.utils.helper_methods import object_to_str


class OutgoingEmail:
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

    def to_serializable_json(self):
        return {
            'from': self.sender,
            'to': self.to,
            'subject': self.subject,
            'mimeType': self.mime_type,
            'body': self.body
        }