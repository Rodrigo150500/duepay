import os
from .unzip_file import unzip_file

def test_unzip_file():
  
  file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/duepay/sales_data/NFC 31.10.2025 16-40.zip"))

  buffer = unzip_file(file_path)

  assert isinstance(buffer, list)




