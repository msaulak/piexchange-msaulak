

import argparse

from src.lib.outgoing_email_manager import OutgoingEmailManager


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('email_template', help='Path to the email template JSON file')
    parser.add_argument('customers_data', help='Path to the customer data file')
    parser.add_argument('output_directory', help='Path where outgoing email JSON should be saved')
    parser.add_argument('errors_file_path', help='Path to where erroneous records should be saved.')

    return parser.parse_args()

def run_email_manager():
    args = parse_args()
    print(args)
    x = OutgoingEmailManager(email_template_path=args.email_template, customer_data_path=args.customers_data,
                             output_emails_directory=args.output_directory, errors_file_location=args.errors_file_path)


if __name__ == '__main__':
    run_email_manager()
