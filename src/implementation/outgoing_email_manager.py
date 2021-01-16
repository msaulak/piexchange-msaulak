import logging
import os
from pathlib import Path

from src.customer_data_extractors.csv_customer_data_extractor import CsvCustomerDataExtractor
from src.lib.email_template import EmailTemplate
from src.utils.custom_exceptions import InvalidCustomerDataExtractor

logger = logging.getLogger('pi.exchange.emailsender')

CUSTOMER_DATA_EXTRACTOR_FACTORY = {
    '.csv' : CsvCustomerDataExtractor
}

def customer_data_extractor_factory(customer_data_path: str):
    file_extension = ''.join(Path(customer_data_path).suffixes)

    try:
        return CUSTOMER_DATA_EXTRACTOR_FACTORY[file_extension](customer_data_path)
    except KeyError as e:
        logger.error(e)
        raise InvalidCustomerDataExtractor(f'No customer data extractor found for file type {file_extension}. '
                                           f'File {customer_data_path}')


class OutgoingEmailManager:
    def __init__(self, email_template_path: str, customer_data_path: str,
                 output_emails_directory: str, errors_file_location: str):

        self.customer_data_path = customer_data_path

        self.output_emails_directory = output_emails_directory
        self.errors_file_location = errors_file_location
        self.email_template_path: str = email_template_path
        self.email_template: EmailTemplate = EmailTemplate()
        self.customer_data_extractor = customer_data_extractor_factory(customer_data_path)

    def read_data(self):
        self.email_template.load_template_from_file(self.email_template_path)
        self.customer_data_extractor.load_customer_data()
