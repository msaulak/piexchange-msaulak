import logging
from typing import Optional

import pandas as pd

from src.lib.base_customer_data_extractor import BaseCustomerDataExtractor

logger = logging.getLogger('pi.exchange.emailsender')

class CsvCustomerDataExtractor(BaseCustomerDataExtractor):
    def __init__(self, customer_data_csv_path: str):
        super(CsvCustomerDataExtractor, self).__init__()

        self.customer_data_csv_path = customer_data_csv_path
        self.customer_data: Optional[pd.DataFrame] = None

    def load_customer_data(self):
        self.customer_data = pd.read_csv(self.customer_data_csv_path)

        logger.info(self.customer_data)
