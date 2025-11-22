from io import BytesIO
from pandas import DataFrame

from .interface.duepay_use_case_interface import DuepayUseCaseInterface

from src.services.duepay_service import DuepayService
from src.services.sales_service import SalesService

from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse

from src.validations.mime_type_validation import mime_type_validation
from src.errors.types.http_bad_request import HttpBadRequest
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntity

class DuepayUseCase(DuepayUseCaseInterface):
  
  def generate_report(self, http_request: HttpRequest) -> HttpResponse:

    try:

      sales_xml = http_request.body["xml"]
      duepay_csv = http_request.body["csv"]

      if mime_type_validation(sales_xml) == False or mime_type_validation(duepay_csv) == False: raise HttpBadRequest("Erro: verifique os arquivos enviados")

      dataframe_sales = SalesService().generate_sales_df_cpf_total_chave(sales_xml)
      dataframe_duepay = DuepayService().generate_duepay_df_total(duepay_csv) 
      
      report = self.__merge_dataframe_sales_and_duepay(dataframe_sales, dataframe_duepay)

      excel_report_buffer = self.__export_dataframe(report)

      formatted_response = self.__formatted_response(excel_report_buffer)

      return formatted_response
    
    except Exception as exception:

      print(f"Error:{str(exception)}")

      raise HttpUnprocessableEntity("Error: Verifique os arquivos enviados")
    

  def __merge_dataframe_sales_and_duepay(self, dataframe_sales: DataFrame, dataframe_duepay: DataFrame) -> DataFrame:

    dataframe_merge = dataframe_duepay.merge(dataframe_sales, left_on="Valor", right_on="Total", how='outer')

    dataframe_merge_filled = dataframe_merge.fillna("Verificar").infer_objects(copy=False)

    return dataframe_merge_filled
  
  
  def __export_dataframe(self, report: DataFrame) -> BytesIO:

    buffer = BytesIO()

    report.to_excel(buffer,index=False)

    buffer.seek(0)

    return buffer
  

  def __formatted_response(self, excel_report_buffer: BytesIO) -> HttpResponse:
    return HttpResponse(
      body=excel_report_buffer,
      status_code=200
    )