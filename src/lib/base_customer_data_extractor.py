"""Module to represent the base class customer data extractor."""
import logging
import os

import pandas as pd
from typing import Optional, List

from src.lib.customer_data import CustomerData
from src.utils.custom_exceptions import InvalidCustomerData
from src.utils.helper_methods import log_and_call

logger = logging.getLogger('pi.exchange.emailsender')


class BaseCustomerDataExtractor:
    """Base class for extracting customer data. This class does not load the customer data; that task must
    be implemented by the inheritor. An instance of this class stores customer data in a dataframe and cleans it.
    The assumption here is that a customer data record with any missing field is a bad record and will be recorded
    as an error. This can be modified by editing line with comment #filterallbadrecords."""

    def __init__(self, data_file_path: str, errors_file_path: str):
        self.data_file_path: str = data_file_path
        self.errors_file_path: str = errors_file_path

        self.customer_data: Optional[pd.DataFrame] = None
        self.erroneous_data: Optional[pd.DataFrame] = None

        self._customer_data_list: List[CustomerData] = []

    @property
    @log_and_call
    def customer_data_list(self) -> List[CustomerData]:
        """Property of an object
        Returns:
            List[CustomerData]: List of customer data
        """
        return self._customer_data_list

    @log_and_call
    def _load_customer_data(self) -> pd.DataFrame:
        """Method must be implemented by the inheritor.
        Returns:
            pd.DataFrame: Customer record as a dataframe.
        """
        raise NotImplementedError('load_customer_data not implemented')

    @log_and_call
    def _clean_dataset(self) -> None:
        """Remove erroneous records and saves that at the user given location.
        Currently, this method removes all records which have ANY missing customer data field. This can
        be modified to remove records with missing only email be replacing the line

        self.erroneous_data = self.customer_data[self.customer_data.isnull().any(axis=1)]
        with
        self.erroneous_data = self.customer_data[self.customer_data['EMAIL'].isna()]
        Returns:
            None

        """
        self.erroneous_data = self.customer_data[self.customer_data.isnull().any(axis=1)]  # filterallbadrecords
        logger.info(f'Erroneous records\n{self.erroneous_data}')
        # Write to file
        error_file_directory = os.path.dirname(self.errors_file_path)

        logger.info(f'Creating directories upto {error_file_directory}')
        os.makedirs(error_file_directory, exist_ok=True)

        logger.info(f'Exporting erroneous records to {self.errors_file_path}')
        self.erroneous_data.to_csv(self.errors_file_path, index=False)

        # Overwrite customer data without the erroneous records
        self.customer_data.dropna(inplace=True)

    @log_and_call
    def load_dataset(self) -> None:
        """Method loads customer dataset from given csv and cleans the dataset.
        Returns:
            None
        """
        self.customer_data = self._load_customer_data()
        logger.info(f'Customer dataframe\n{self.customer_data}')
        self._clean_dataset()
        logger.info(f'Cleaned customer data\n{self.customer_data}')
        try:
            for customer_data_dict in self.customer_data.to_dict(orient='records'):
                self._customer_data_list.append(CustomerData(**customer_data_dict))
        except KeyError as e:
            logger.error(e)
            raise InvalidCustomerData(f'Customer data missing field {e}')
