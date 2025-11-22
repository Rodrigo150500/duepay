from flask import Blueprint, request, send_file, jsonify, render_template
from src.main.http_types.http_request.http_request import HttpRequest
from src.use_case.duepay_use_case import DuepayUseCase
from src.use_case.search_xml_use_case import SearchForXML
from src.errors.error_handler import error_handler

duepay_bp = Blueprint("duepay_bp_route", __name__)

@duepay_bp.route("/duepay", methods=["POST"])
def send_duepay_report():
  try:

    xml_file = request.files["sales"]
    csv_file = request.files["duepay"]


    http_request = HttpRequest(
      body={
        "csv": csv_file,
        "xml": xml_file
      }
    )

    use_case = DuepayUseCase()

    response = use_case.generate_report(http_request)

    return send_file(
        response.body,
        as_attachment=True,
        download_name="relatorio_duepay.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ), response.status_code
      
  except Exception as exception:

    print(f"Error: {str(exception)}")

    response = error_handler(exception)

    return jsonify(response.body), response.status_code
  

@duepay_bp.route("/duepay_page", methods=["GET", "POST"])
def show_duepay_forms():
  return render_template("duepay/index.html")


@duepay_bp.route("/duepay_search_xml", methods=["POST"])
def search_duepay_xml():
    try:
        xml_file = request.files["xml"]
        cpf_or_total = request.form["cpf_or_total"]

        http_request = HttpRequest(
            body={
                "xml": xml_file,
                "value": cpf_or_total
            }
        )

        use_case = SearchForXML()

        response = use_case.search(http_request)

        return jsonify(response.body), response.status_code

    except Exception as exception:
        
        print(f"Error: {str(exception)}")

        response = error_handler(exception)

        return jsonify(response.body), response.status_code