"""Module implementing the primary processing class, following composite design pattern."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Type, Optional

from src.customer_data_extractors.csv_customer_data_extractor import CsvCustomerDataExtractor
from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor
from src.lib.customer_data import CustomerData
from src.lib.email_template import EmailTemplate
from src.lib.outgoing_email import OutgoingEmail
from src.lib.outgoing_email_api import OutgoingEmailApi
from src.utils.custom_exceptions import InvalidCustomerDataExtractor
from src.utils.helper_methods import log_and_call

logger = logging.getLogger('pi.exchange.emailsender')

# Cheap Factory Method implementation
CUSTOMER_DATA_EXTRACTOR_FACTORY = {
    '.csv': CsvCustomerDataExtractor
}


def customer_data_extractor_factory(customer_data_path: str) -> Type[BaseCustomerDataExtractor]:
    """Factory returning the data customer extraction class based on the data file extension.
    This is a cheap factory implementation where instantiation is not done. This method can be extended
    to sources like databases, network locations, rest apis.
    Args:
        customer_data_path(str): Absolute path to the customer data file

    Returns:
        Type[BaseCustomerDataExtractor]: Returns an implementation of BaseCustomerDataExtractor

    Raises:
        InvalidCustomerDataExtractor: When the extension of the file has no linked implementation.
    """
    file_extension = ''.join(Path(customer_data_path).suffixes)

    try:
        return CUSTOMER_DATA_EXTRACTOR_FACTORY[file_extension]
    except KeyError as e:
        logger.error(e)
        raise InvalidCustomerDataExtractor(f'No customer data extractor found for file type {file_extension}. '
                                           f'File {customer_data_path}')


class OutgoingEmailManager:
    """Class encapsulating the central processing manager."""

    def __init__(self, email_template_path: str, customer_data_path: str,
                 output_emails_directory: str, errors_file_location: str,
                 email_sending_api: OutgoingEmailApi = None):
        """
        Initialize the instance
        Args:
            email_template_path: Path the json file with the email template
            customer_data_path: Path the file with customer data
            output_emails_directory: Path the where merged emails are to be serialized
            errors_file_location: Path where erroneous records are to be serialized
            email_sending_api: Which implementation to use to send emails Not yet implemented.
        """

        self.customer_data_path: str = customer_data_path

        self.output_emails_directory: str = output_emails_directory
        self.errors_file_location: str = errors_file_location
        self.email_template_path: str = email_template_path
        self.email_template: EmailTemplate = EmailTemplate()

        self.email_sending_api: Optional[OutgoingEmailApi] = email_sending_api

        customer_data_extractor_class: Type[BaseCustomerDataExtractor] = customer_data_extractor_factory(
            customer_data_path)
        self.customer_data_extractor: BaseCustomerDataExtractor = customer_data_extractor_class(customer_data_path,
                                                                                                errors_file_location)

        self.outgoing_emails: List[OutgoingEmail] = []

        self.today: str = datetime.now().strftime('%d %b %Y')  # Capture today for filling email template

    @log_and_call
    def _load_data(self) -> None:
        """Private method to load email template and customer data. The customer data is loaded using the 
        extractor given during init.
        Returns:
            None
        """
        self.email_template.load_template_from_file(self.email_template_path)
        self.customer_data_extractor.load_dataset()

    @log_and_call
    def _get_replaced_field(self, template_field: str, customer_data: CustomerData) -> str:
        """Replaces the template placeholders with customer data.
        Args:
            template_field (str): field from the email template like {{FIRST_NAME}}
            customer_data (CustomerData): Instance of customer data to use for filling template

        Returns:
            str: string after replacing email template placeholders with customer data
        """
        template_field_data = getattr(self.email_template, template_field)
        template_field_data = template_field_data.replace(EmailTemplate.filler_first_name, customer_data.first_name)
        template_field_data = template_field_data.replace(EmailTemplate.filler_last_name, customer_data.last_name)
        template_field_data = template_field_data.replace(EmailTemplate.filler_title, customer_data.title)
        template_field_data = template_field_data.replace(EmailTemplate.filler_today, self.today)

        return template_field_data

    @log_and_call
    def _merge_template_with_customer_data(self) -> None:
        """Private method to iteratively merge email template with customer dataset
        Returns:
            None
        """
        for customer_data in self.customer_data_extractor.customer_data_list:
            outgoing_email = OutgoingEmail(sender=self.email_template.sender, to=customer_data.email,
                                           subject=self._get_replaced_field('subject', customer_data),
                                           mime_type=self.email_template.mime_type,
                                           body=self._get_replaced_field('body', customer_data))

            self.outgoing_emails.append(outgoing_email)

    @log_and_call
    def _export_emails_to_folder(self) -> None:
        """Serialize merged emails which are instances of OutgoingEmail class
        Returns:
            None
        """
        # Create folder with current datetime
        output_dir_for_run = os.path.join(self.output_emails_directory, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        os.makedirs(output_dir_for_run, exist_ok=True)

        for outgoing_email in self.outgoing_emails:
            file_name = f'output_email_{outgoing_email.to}.json'
            with open(os.path.join(output_dir_for_run, file_name), 'w') as fp:
                fp.write('\n')  # The sample data given by pi exchange had an empty line, hence this.
                json.dump(outgoing_email.to_serializable_json(), fp, indent=4)

    @log_and_call
    def _final_send(self) -> None:
        """Send out emails using the user selection between SMTP or REST API.
        Required implementing RESTOutgoingEmailApi.send_message or SMTPOutgoingEmailApi.send_message
        Returns:
            None
        """
        if self.email_sending_api is not None:
            for outgoing_email in self.outgoing_emails:
                self.email_sending_api.send_message(outgoing_email)

    @log_and_call
    def send_emails(self):
        """Method to encapsulate all private methods which perform the following in the given order:
            1. load email template
            2. load customer data
            3. merge 1 & 2
            4. serialize outgoing emails
            5. send emails
        Returns:

        """
        self._load_data()
        self._merge_template_with_customer_data()
        self._export_emails_to_folder()
        self._final_send()
