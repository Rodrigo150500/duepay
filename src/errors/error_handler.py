from .types.http_bad_request import HttpBadRequest
from .types.http_error_server import HttpErrorServer
from .types.http_unprocessable_entity import HttpUnprocessableEntity
from src.main.http_types.http_response.http_response import HttpResponse

def error_handler(error):

    if (isinstance(error, (HttpErrorServer, HttpBadRequest, HttpUnprocessableEntity))):

        return HttpResponse(
            body={
                "error": {
                    "message": error.message,
                    "name": error.name
                }
            }, 
            status_code= error.status_code
        )

    else:
        return HttpResponse(
            body={
                "error": {
                    "message": "Falha em nosso servidor",
                    "name": "Error Server"
                }
            }, status_code=500
        )