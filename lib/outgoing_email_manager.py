from lib.base_customer_data_extractor import BaseCustomerDataExtractor


class OutgoingEmailManager:
    def __init__(self, email_template: str, customer_data_extractor: BaseCustomerDataExtractor,
                 output_email_location: str, errors_file_location: str = None):

        self.email_template = email_template
        self.customer_data_extractor = customer_data_extractor

        self.output_email_location = output_email_location
        self.errors_file_location = errors_file_location if errors_file_location is not None else output_email_location

        self.sender = None
        self.mime_type = None

        self.init_email_template()

    def init_email_template(self):
        pass

