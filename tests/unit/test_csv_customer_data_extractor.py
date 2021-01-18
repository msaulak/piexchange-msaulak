import os
from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

from src.customer_data_extractors.csv_customer_data_extractor import CsvCustomerDataExtractor
from src.utils.helper_methods import get_parent_dir


class TestCsvCustomerDataExtractor(TestCase):

    @patch('src.lib.base_customer_data_extractor.BaseCustomerDataExtractor')
    def test__load_customer_data(self, _):
        self.csv_customer_data_extractor = CsvCustomerDataExtractor('', '')
        self.csv_customer_data_extractor.data_file_path = os.path.join(get_parent_dir(__file__, 2), 'data',
                                                                       'customers.csv')

        actual_customer_data = OrderedDict(self.csv_customer_data_extractor._load_customer_data().fillna(0).to_dict(orient='dict'))
        expected_customer_data = OrderedDict([('TITLE', {0: 'Mr', 1: 'Mrs', 2: 'Mrs', 3: 'Mrs', 4: 'Mrs'}),
                                              ('FIRST_NAME', {0: 'John', 1: 'Michelle', 2: 'Sam', 3: 'AAA', 4: 0}),
                                              ('LAST_NAME', {0: 'Smith', 1: 'Smith', 2: 'Martha', 3: 0, 4: 0}),
                                              ('EMAIL', {0: 'john.smith@example.com', 1: 'michelle.smith@example.com',
                                                         2: 0, 3: 'BBB', 4: 0})])

        self.assertEqual(expected_customer_data, actual_customer_data)
