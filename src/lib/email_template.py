import json
import logging
from typing import Dict, Optional

from src.utils.helper_methods import log_and_call, object_to_str

logger = logging.getLogger('pi.exchange.emailsender')

class EmailTemplate:
    def __init__(self):
        self.sender: Optional[str] = None
        self.subject: Optional[str] = None
        self.mime_type: Optional[str] = None
        self.body: Optional[str] = None

    def load_template_from_file(self, email_template_path: str):
        with open(email_template_path) as fp_email_template:
            email_template: Dict[str, str] = json.load(fp_email_template)
            logger.info(f'Loaded {email_template} from file {email_template_path}')
            self.sender= email_template['from']
            self.subject = email_template['subject']
            self.mime_type = email_template['mimeType']
            self.body = email_template['body']

            logger.info(f'EmailTemplate: {str(self)}')

    def __str__(self):
        return object_to_str(self)

    def __repr__(self):
        return object_to_str(self)
