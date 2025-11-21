import os
from pandas import DataFrame

from .sales_service import SalesService

def test_sales_service():
  
  xml_zip = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/sales_data/NFC 31.10.2025 16-40.zip"))

  sales_service = SalesService()
  sales_dataframe = sales_service.generate_sales_df_cpf_total_chave(xml_zip)

  assert isinstance(sales_dataframe, DataFrame)
  assert not sales_dataframe.empty

