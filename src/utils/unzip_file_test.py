import os
from .unzip_file import unzip_file

def test_unzip_file():
  
  file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/sales_data/SAT 08.08.2025 17-47.zip"))

  buffer = unzip_file(file_path)

  assert isinstance(buffer, list)




