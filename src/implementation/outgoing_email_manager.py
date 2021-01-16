import logging
import os
from pathlib import Path

from src.customer_data_extractors.csv_customer_data_extractor import CsvCustomerDataExtractor
from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor
from src.lib.email_template import EmailTemplate
from src.utils.custom_exceptions import InvalidCustomerDataExtractor

logger = logging.getLogger('pi.exchange.emailsender')

CUSTOMER_DATA_EXTRACTOR_FACTORY = {
    '.csv' : CsvCustomerDataExtractor
}

def customer_data_extractor_factory(customer_data_path: str):
    file_extension = ''.join(Path(customer_data_path).suffixes)

    try:
        return CUSTOMER_DATA_EXTRACTOR_FACTORY[file_extension]
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

        customer_data_extractor_class = customer_data_extractor_factory(customer_data_path)
        self.customer_data_extractor: BaseCustomerDataExtractor = customer_data_extractor_class(customer_data_path,
                                                                                                errors_file_location)

    def _load_data(self):
        self.email_template.load_template_from_file(self.email_template_path)
        self.customer_data_extractor.load_dataset()

    def _merge_template_with_customer_data(self):
        pass

    def _export_emails_to_folder(self):
        pass

    def _final_send(self):
        pass

    def send_emails(self):
        self._load_data()
        self._merge_template_with_customer_data()
        self._export_emails_to_folder()
        self._final_send()
