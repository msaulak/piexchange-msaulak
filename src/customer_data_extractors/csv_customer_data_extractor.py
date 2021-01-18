"""Implementation of BaseCustomerDataExtractor for csv files"""

import logging

import pandas as pd

from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor
from src.utils.helper_methods import log_and_call

logger = logging.getLogger('pi.exchange.emailsender')


class CsvCustomerDataExtractor(BaseCustomerDataExtractor):
    """Implementation of BaseCustomerDataExtractor for csv files"""
    def __init__(self, customer_data_csv_path: str, errors_file_path: str):
        super(CsvCustomerDataExtractor, self).__init__(customer_data_csv_path, errors_file_path)

    @log_and_call
    def _load_customer_data(self) -> pd.DataFrame:
        """Overrides BaseCustomerDataExtractor._load_customer_data for loading customer data
        from csv files.
        Returns:
            pd.DataFrame: Customer data
        """
        customer_data: pd.DataFrame = pd.read_csv(self.data_file_path)
        logger.info(f'Raw dat\n{customer_data}')
        return customer_data
