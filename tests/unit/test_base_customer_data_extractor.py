import os
from collections import OrderedDict
from unittest import TestCase
from unittest.mock import Mock, patch

from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor
from src.utils.helper_methods import get_parent_dir

import pandas as pd

pickled_customer_file = os.path.join(get_parent_dir(__file__, 2), 'data', 'customer_data.pkl')


class TestBaseCustomerDataExtractor(TestCase):

    def setUp(self) -> None:
        self.test_data_file_path = os.path.join(get_parent_dir(__file__, 2), 'data', 'customers.csv')
        self.errors_file_path = os.path.join(get_parent_dir(__file__, 2), 'data', 'errors.csv')
        self.base_customer_extractor = BaseCustomerDataExtractor(data_file_path=self.test_data_file_path,
                                                                 errors_file_path=self.errors_file_path)

    def tearDown(self) -> None:
        if os.path.exists(self.errors_file_path):
            os.remove(self.errors_file_path)

    @patch('src.lib.base_customer_data_extractor.BaseCustomerDataExtractor._load_customer_data',
           return_value=pd.read_pickle(pickled_customer_file))
    def test_customer_data_list(self, _):
        self.base_customer_extractor.load_dataset()
        actual = str(self.base_customer_extractor.customer_data_list)
        expected = '[title : Mr | first_name : John | last_name : Smith | email : john.smith@example.com | full_name ' \
                   ': John Smith, title : Mrs | first_name : Michelle | last_name : Smith | email : ' \
                   'michelle.smith@example.com | full_name : Michelle Smith]'

        self.assertEqual(expected, actual)

    @patch('src.lib.base_customer_data_extractor.BaseCustomerDataExtractor._load_customer_data',
           return_value=pd.read_pickle(pickled_customer_file))
    def test__clean_dataset(self, _):
        self.base_customer_extractor.load_dataset()

        actual_erroneous_dataset = OrderedDict(
            self.base_customer_extractor.erroneous_data.fillna(0).to_dict(orient='dict'))
        expected_erroneous_dataset = OrderedDict(
            [('TITLE', {2: 'Mrs', 3: 'Mrs', 4: 'Mrs'}), ('FIRST_NAME', {2: 'Sam', 3: 'AAA', 4: 0}),
             ('LAST_NAME', {2: 'Martha', 3: 0, 4: 0}), ('EMAIL', {2: 0, 3: 'BBB', 4: 0})])
        self.assertEqual(expected_erroneous_dataset, actual_erroneous_dataset)

        actual_cleaned_data = OrderedDict(self.base_customer_extractor.customer_data.to_dict(orient='dict'))
        expected_cleaned_data = OrderedDict([('TITLE', {0: 'Mr', 1: 'Mrs'}), ('FIRST_NAME', {0: 'John', 1: 'Michelle'}),
                                             ('LAST_NAME', {0: 'Smith', 1: 'Smith'}),
                                             ('EMAIL', {0: 'john.smith@example.com', 1: 'michelle.smith@example.com'})])
        self.assertEqual(expected_cleaned_data, actual_cleaned_data)

    def _load_customer_data(self):
        self.assertRaises(NotImplementedError, self.base_customer_extractor._load_customer_data)

    def test_load_dataset(self):
        self.base_customer_extractor._load_customer_data = Mock(return_value=pd.DataFrame())
        self.base_customer_extractor._clean_dataset = Mock()

        self.base_customer_extractor.load_dataset()

        self.base_customer_extractor._load_customer_data.assert_called_once()
        self.base_customer_extractor._clean_dataset.assert_called_once()
