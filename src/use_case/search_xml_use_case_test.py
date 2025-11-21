import os
from .search_xml_use_case import SearchForXML
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse

def test_search_for_xml():

    use_case = SearchForXML()

    http_request = HttpRequest(
        body={
            "xml": os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/sales_data/SAT 08.08.2025 17-47.zip")),
            "value":29.5
            }
    )

    response = use_case.search(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert len(response.body["data"]) == 2