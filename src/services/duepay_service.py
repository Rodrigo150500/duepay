import xml.etree.ElementTree as ET
from pandas import DataFrame
from .interface.duepay_service_interface import DuepayServiceInterface

class DuepayService(DuepayServiceInterface):

  def generate_duepay_df_total(self, xls_file) -> DataFrame:

    data_extracted_dict = self.__extract_total_from_xls(xls_file)

    dataframe_duepay = DataFrame(data_extracted_dict)
    
    return dataframe_duepay
  
  def __extract_total_from_xls(self, xls_file) -> dict:
        
      tree = ET.parse(xls_file)
      root = tree.getroot()

      total = []

      namespace = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

      for row in root.findall(".//ss:Row", namespace):
        cells = row.findall(".//ss:Cell", namespace)
        if len(cells) >= 4:  # garante que tem pelo menos 4 colunas
            data_elem = cells[3].find(".//ss:Data", namespace)
            if data_elem is not None and data_elem.text:
                valor_str = data_elem.text.strip().replace(",", ".")
                try:
                    total.append(float(valor_str))
                except ValueError:
                    pass  # ignora se não for 

      total_column = {"Valor": total}

      return total_column

  

