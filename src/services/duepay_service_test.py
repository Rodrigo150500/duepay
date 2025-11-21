import os
from pandas import DataFrame
from .duepay_service import DuepayService

def test_duepay_service():

  duepay_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/duepay_data/Relatorio de Movimentacao Diaria.xls"))

  duepay_service = DuepayService()

  duepay_dataframe = duepay_service.generate_duepay_df_total(duepay_file)

  assert isinstance(duepay_dataframe, DataFrame)
  assert not duepay_dataframe.empty

