from pandas import DataFrame
from abc import ABC, abstractmethod

class DuepayServiceInterface(ABC):

  @abstractmethod
  def generate_duepay_df_total(self, csv_file) -> DataFrame:
    pass