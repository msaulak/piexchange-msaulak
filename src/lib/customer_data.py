"""Module to represent a customer data for email sending purposes."""
from src.utils.helper_methods import object_to_str


class CustomerData:
    """Simple class to encapsulate a customers information."""

    def __init__(self, **customer_data_dict):
        self.title = customer_data_dict['TITLE']
        self.first_name = customer_data_dict['FIRST_NAME']
        self.last_name = customer_data_dict['LAST_NAME']
        self.email = customer_data_dict['EMAIL']

        self.full_name = ' '.join([self.first_name, self.last_name])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return object_to_str(self)
