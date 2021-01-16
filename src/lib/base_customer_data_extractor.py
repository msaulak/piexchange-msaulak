import logging
import os

import pandas as pd
from typing import Optional

logger = logging.getLogger('pi.exchange.emailsender')


class BaseCustomerDataExtractor:
    def __init__(self, data_file_path: str, errors_file_path: str):
        self.data_file_path: str = data_file_path
        self.errors_file_path: str = errors_file_path

        self.customer_data: Optional[pd.DataFrame] = None
        self.erroneous_data: Optional[pd.DataFrame] = None

    def _load_customer_data(self):
        raise NotImplementedError('load_customer_data not implemented')

    def _clean_dataset(self):
        self.erroneous_data = self.customer_data[self.customer_data.isnull().any(axis=1)]
        logger.info(f'Erroneous records\n{self.erroneous_data}')
        # Write to file
        error_file_directory = os.path.dirname(self.errors_file_path)

        logger.info(f'Creating directories upto {error_file_directory}')
        os.makedirs(error_file_directory, exist_ok=True)

        logger.info(f'Exporting erroneus records to {self.errors_file_path}')
        self.erroneous_data.to_csv(self.errors_file_path, index=False)

        # Overwrite customer data without the erroneous records
        self.customer_data.dropna(inplace=True)

    def load_dataset(self):
        self.customer_data = self._load_customer_data()
        logger.info(f'Customer dataframe\n{self.customer_data}')
        self._clean_dataset()
        logger.info(f'Cleaned customer data\n{self.customer_data}')
