import argparse
import logging
import sys
from typing import Optional

from src.implementation.outgoing_email_manager import OutgoingEmailManager
from src.outgoing_email_impl.rest_outgoing_email_api import RESTOutgoingEmailApi
from src.outgoing_email_impl.smtp_outgoing_email_api import SMTPOutgoingEmailApi
from src.lib.outgoing_email_api import OutgoingEmailApi
from src.utils.custom_exceptions import *

logger = logging.getLogger('pi.exchange.emailsender')


def parse_args():
    parser = argparse.ArgumentParser()

    # flags can be added to each of the arguments below to be able to pass them in any order
    parser.add_argument('email_template', help='Path to the email template JSON file')
    parser.add_argument('customers_data', help='Path to the customer data file')
    parser.add_argument('output_directory', help='Path where outgoing email JSON should be saved')
    parser.add_argument('errors_file_path', help='Path to where erroneous records should be saved.')

    sending_api_parser = parser.add_subparsers(dest='send', title='Send emails',
                                               description='Optional. Instruct on which api to use to send emails.',
                                               help='Optional. Instruct on which api to use to send emails.')

    sending_api_subparser = sending_api_parser.add_parser('send', help='Send email via an API')
    sending_api_group = sending_api_subparser.add_mutually_exclusive_group(required=True)

    sending_api_group.add_argument('--smtp', action='store_true')
    sending_api_group.add_argument('--rest', action='store_true')

    return parser.parse_args()


def run_email_manager():
    args = parse_args()
    logger.info(args)

    email_sending_api: Optional[OutgoingEmailApi] = None
    # Ideally, use a Factory here.
    if args.send is not None:
        email_sending_api = RESTOutgoingEmailApi() if args.rest else SMTPOutgoingEmailApi()

    outgoing_email_manager: OutgoingEmailManager = OutgoingEmailManager(email_template_path=args.email_template,
                                                                        customer_data_path=args.customers_data,
                                                                        output_emails_directory=args.output_directory,
                                                                        errors_file_location=args.errors_file_path,
                                                                        email_sending_api=email_sending_api)

    try:
        outgoing_email_manager.send_emails()
    except (InvalidCustomerDataExtractor, InvalidEmailTemplate, InvalidCustomerData) as e:
        logger.error(f'Fatal Error: {type(e).__name__}: {e}')
        sys.exit(-1)


if __name__ == '__main__':
    run_email_manager()
