import os
from io import BytesIO
from src.validations.mime_type_validation.mime_type_validation import mime_type_validation


def test_validate_files_sucessfully():

    xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/sales_data/NFC 31.10.2025 16-40.zip"))
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/duepay/duepay_data/Relatorio de Movimentacao Diaria.xls"))
    
    # Testa se os arquivos realmente existem
    assert os.path.exists(xml_path)
    assert os.path.exists(csv_path)

    # Extrai apenas o nome do arquivo
    xml_filename = os.path.basename(xml_path)
    csv_filename = os.path.basename(csv_path)

    # Testa a validação
    assert mime_type_validation(xml_filename) is True
    assert mime_type_validation(csv_filename) is True