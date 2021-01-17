import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List

from src.customer_data_extractors.csv_customer_data_extractor import CsvCustomerDataExtractor
from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor
from src.lib.customer_data import CustomerData
from src.lib.email_template import EmailTemplate
from src.lib.outgoing_email import OutgoingEmail
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

        self.outgoing_emails: List[OutgoingEmail] = []

        self.today = datetime.now().strftime('%d %b %Y')

    def _load_data(self):
        self.email_template.load_template_from_file(self.email_template_path)
        self.customer_data_extractor.load_dataset()

    def _get_replaced_field(self, template_field, customer_data: CustomerData):
        template_field_data = getattr(self.email_template, template_field)
        template_field_data = template_field_data.replace(EmailTemplate.filler_first_name, customer_data.first_name)
        template_field_data = template_field_data.replace(EmailTemplate.filler_last_name, customer_data.last_name)
        template_field_data = template_field_data.replace(EmailTemplate.filler_title, customer_data.title)
        template_field_data = template_field_data.replace(EmailTemplate.filler_today, self.today)

        return template_field_data

    def _merge_template_with_customer_data(self):
        for customer_data in self.customer_data_extractor.customer_data_list:
            outgoing_email = OutgoingEmail(sender=self.email_template.sender, to=customer_data.email,
                                           subject=self._get_replaced_field('subject', customer_data),
                                           mime_type=self.email_template.mime_type,
                                           body=self._get_replaced_field('body', customer_data))

            self.outgoing_emails.append(outgoing_email)


    def _export_emails_to_folder(self):
        # Create folder with current datetime
        output_dir_for_run = os.path.join(self.output_emails_directory, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        os.makedirs(output_dir_for_run, exist_ok=True)

        for outgoing_email in self.outgoing_emails:
            file_name = f'output_email_{outgoing_email.to}.json'
            with open(os.path.join(output_dir_for_run, file_name), 'w') as fp:
                fp.write('\n')
                json.dump(outgoing_email.to_serializable_json(), fp, indent=4)

    def _final_send(self):
        pass

    def send_emails(self):
        self._load_data()
        self._merge_template_with_customer_data()
        self._export_emails_to_folder()
        self._final_send()
