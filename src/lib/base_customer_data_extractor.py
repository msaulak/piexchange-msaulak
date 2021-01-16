import logging
import os

import pandas as pd
from typing import Optional
logger = logging.getLogger('pi.exchange.emailsender')

class BaseCustomerDataExtractor:
    def __init__(self, data_file_path: str, errors_file_path: str):
        self.data_file_path:str = data_file_path
        self.errors_file_path:str = errors_file_path

        self.customer_data: Optional[pd.DataFrame] = None
        self.erroneous_data: Optional[pd.DataFrame] = None

    def _load_customer_data(self):
        raise NotImplementedError('load_customer_data not implemented')

    def _clean_dataset(self):
        self.erroneous_data = self.customer_data[self.customer_data.isnull().any(axis=1)]

        # Write to file
        error_file_directory = os.path.dirname(self.errors_file_path)
        print(error_file_directory)
        os.makedirs(error_file_directory, exist_ok=True)

        self.erroneous_data.c

    def load_dataset(self):
        self.customer_data = self._load_customer_data()
        logger.info(f'Customer data\n{self.customer_data}')
        self._clean_dataset()