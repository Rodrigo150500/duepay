from pandas import DataFrame
from abc import ABC, abstractmethod

class SalesServiceInterface(ABC):
  
  @abstractmethod
  def generate_sales_df_cpf_total_chave(self, xml_zip) -> DataFrame:
      pass