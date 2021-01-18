"""Module representing an Email template."""
import json
import logging
from typing import Dict, Optional

from src.utils.custom_exceptions import InvalidEmailTemplate
from src.utils.helper_methods import log_and_call, object_to_str

logger = logging.getLogger('pi.exchange.emailsender')


class EmailTemplate:
    """Class encapsulating an email template. Data can loaded from a json file using the load_template_from_file
    method. Class variables represent placeholders in an email template.
    This class can be made into an abstract class with load_template_from_file as an abstract method."""
    filler_first_name = '{{FIRST_NAME}}'
    filler_last_name = '{{LAST_NAME}}'
    filler_title = '{{TITLE}}'
    filler_today = '{{TODAY}}'

    def __init__(self):
        self.sender: Optional[str] = None
        self.subject: Optional[str] = None
        self.mime_type: Optional[str] = None
        self.body: Optional[str] = None

    @log_and_call
    def load_template_from_file(self, email_template_path: str) -> None:
        """Method reads a json file and loads it into an instance of EmailTemplate.
        Does not validate if the file exists or not.
        Args:
            email_template_path: 

        Returns:
            None

        Raises:
            InvalidEmailTemplate: If the template is malformed.
            FileNotFoundError: If the json file does not exist.
            json.decoder.JSONDecodeError: if file can not be read by json loader
        """
        with open(email_template_path) as fp_email_template:
            email_template: Dict[str, str] = json.load(fp_email_template)
            logger.info(f'Loaded {email_template} from file {email_template_path}')

            try:
                self.sender = email_template['from']
                self.subject = email_template['subject']
                self.mime_type = email_template['mimeType']
                self.body = email_template['body']
            except KeyError as e:
                logger.error(e)
                raise InvalidEmailTemplate(f'Email template is missing field {e}')

            logger.info(f'EmailTemplate: {str(self)}')

    def __str__(self):
        return object_to_str(self)

    def __repr__(self):
        return object_to_str(self)
