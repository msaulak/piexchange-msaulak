from unittest import TestCase

from src.lib.customer_data import CustomerData


class TestCustomerData(TestCase):
    def test_init_load(self):
        customer_data = CustomerData(TITLE='Mr', FIRST_NAME='pi', LAST_NAME='exchange',
                                     EMAIL='pi.exchange@pi.exchange.com')
        actual = str(customer_data)
        expected = 'title : Mr | first_name : pi | last_name : exchange | email : pi.exchange@pi.exchange.com | ' \
                   'full_name : pi exchange'

        self.assertEqual(expected, actual)
