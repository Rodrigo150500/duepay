from abc import ABC, abstractmethod
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse

class SearchForXMLInterface(ABC):

    @abstractmethod
    def search(self, http_request: HttpRequest) -> HttpResponse:
        pass