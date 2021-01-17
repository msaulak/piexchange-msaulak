import os
import shutil
from datetime import datetime
from unittest import TestCase, skip
from unittest.mock import Mock, patch, MagicMock

from freezegun import freeze_time

from src.implementation.outgoing_email_manager import OutgoingEmailManager
from src.lib.customer_data import CustomerData
from src.utils.helper_methods import get_parent_dir

@freeze_time(datetime(2021, 1, 14, 1, 1, 1, 1))
class TestOutgoingEmailManager(TestCase):

    def setUp(self) -> None:
        self.test_data_file_path = os.path.join(get_parent_dir(__file__, 2), 'data', 'customers.csv')
        self.errors_file_path = os.path.join(get_parent_dir(__file__, 2), 'data', 'errors.csv')
        self.test_template_file_path = os.path.join(get_parent_dir(__file__, 2), 'data', 'email_template.json')
        self.output_dir = os.path.join(get_parent_dir(__file__, 2), 'data', 'output')

        self.outgoing_email_manager = OutgoingEmailManager(self.test_template_file_path, self.test_data_file_path,
                                                           self.output_dir, self.errors_file_path)

    def tearDown(self) -> None:
        if os.path.exists(self.errors_file_path):
            os.remove(self.errors_file_path)

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test__load_data(self):
        self.outgoing_email_manager.email_template.load_template_from_file = Mock()
        self.outgoing_email_manager.customer_data_extractor.load_dataset = Mock()

        self.outgoing_email_manager._load_data()

        self.outgoing_email_manager.email_template.load_template_from_file.assert_called_once()
        self.outgoing_email_manager.customer_data_extractor.load_dataset.assert_called_once()

    def test__get_replaced_field(self):
        customer_data = CustomerData(TITLE='Mr', FIRST_NAME='pi', LAST_NAME='exchange',
                                     EMAIL='pi.exchange@pi.exchange.com')
        self.outgoing_email_manager.email_template.load_template_from_file(self.test_template_file_path)
        actual = self.outgoing_email_manager._get_replaced_field('subject', customer_data)
        expected = 'pi, a new product is being launched soon...'
        self.assertEqual(expected, actual)

    def test__merge_template_with_customer_data(self):
        self.outgoing_email_manager.email_template.load_template_from_file(self.test_template_file_path)
        self.outgoing_email_manager.customer_data_extractor._customer_data_list = [
            CustomerData(TITLE='Mr', FIRST_NAME='pi', LAST_NAME='exchange', EMAIL='pi.exchange@pi.exchange.com'),
            CustomerData(TITLE='Mrs', FIRST_NAME='pi', LAST_NAME='exchange', EMAIL='mrs.pi.exchange@pi.exchange.com')]

        self.outgoing_email_manager._merge_template_with_customer_data()
        self.assertEqual(len(self.outgoing_email_manager.outgoing_emails), 2)


    def test__export_emails_to_folder(self):
        self.outgoing_email_manager._load_data()
        self.outgoing_email_manager._merge_template_with_customer_data()
        self.outgoing_email_manager._export_emails_to_folder()

        john_smith_file = os.path.join(get_parent_dir(__file__, 2), 'data', 'output', '2021-01-14-01-01-01',
                                         'output_email_john.smith@example.com.json')
        with open(john_smith_file) as fp:
            actual = fp.read()
            expected = '''
{
    "from": "The Marketing Team<marketing@example.com",
    "to": "john.smith@example.com",
    "subject": "John, a new product is being launched soon...",
    "mimeType": "text/plain",
    "body": "Hi Mr John Smith,\\nToday, 14 Jan 2021, we would like to tell you that... Sincerely,\\nThe Marketing Team"
}'''

            self.assertEqual(expected, actual)

    @skip("Skipping since _final_send has not been implemented")
    def test__final_send(self):
        self.fail()

    def test_send_emails(self):
        self.outgoing_email_manager._load_data = Mock()
        self.outgoing_email_manager._merge_template_with_customer_data = Mock()
        self.outgoing_email_manager._export_emails_to_folder = Mock()
        self.outgoing_email_manager._final_send = Mock()

        self.outgoing_email_manager.send_emails()

        self.outgoing_email_manager._load_data.assert_called_once()
        self.outgoing_email_manager._merge_template_with_customer_data.assert_called_once()
        self.outgoing_email_manager._export_emails_to_folder.assert_called_once()
        self.outgoing_email_manager._final_send.assert_called_once()
