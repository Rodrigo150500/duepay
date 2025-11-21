import os
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse
from .duepay_use_case import DuepayUseCase

def test_duepay_use_case():

  sales_file_xml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/sales_data/SAT 08.08.2025 17-47.zip"))

  duepay_file_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/duepay_data/Relatorio de Movimentacao Diaria.xls"))

  duepay_use_case = DuepayUseCase()

  http_request = HttpRequest(
    body={
      "xml": sales_file_xml,
      "csv": duepay_file_csv
    }
  )

  report = duepay_use_case.generate_report(http_request)

  assert isinstance(report, HttpResponse)
  assert report.status_code == 200

