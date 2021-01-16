from src.lib.email_template import EmailTemplate


class OutgoingEmailManager:
    def __init__(self, email_template_path: str, customer_data_path: str,
                 output_emails_directory: str, errors_file_location: str):

        self.customer_data_path = customer_data_path

        self.output_emails_directory = output_emails_directory
        self.errors_file_location = errors_file_location

        self.email_template: EmailTemplate = EmailTemplate(email_template_path)

        print(self.email_template)
