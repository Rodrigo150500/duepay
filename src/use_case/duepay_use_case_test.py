import os
from io import BytesIO
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse
from .duepay_use_case import DuepayUseCase

def test_duepay_use_case():

  sales_file_xml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/duepay/sales_data/NFC 31.10.2025 16-40.zip"))

  duepay_file_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests/duepay/duepay_data/Relatorio de Movimentacao Diaria.xls"))

  with open(sales_file_xml, "rb") as f:
      sales_file_xml_byte = BytesIO(f.read())

  with open(duepay_file_csv, "rb") as f:
      duepay_file_csv_byte = BytesIO(f.read())

  duepay_use_case = DuepayUseCase()

  http_request = HttpRequest(
    body={
      "xml": sales_file_xml_byte,
      "csv": duepay_file_csv_byte
    }
  )

  report = duepay_use_case.generate_report(http_request)

  assert isinstance(report, HttpResponse)
  assert report.status_code == 200

