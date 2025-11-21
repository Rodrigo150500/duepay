from io import BytesIO
from pandas import DataFrame
from .interface.duepay_use_case_interface import DuepayUseCaseInterface
from src.services.duepay.duepay_service import DuepayService
from src.services.duepay.sales_service import SalesService
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse

class DuepayUseCase(DuepayUseCaseInterface):
  
  def generate_report(self, http_request: HttpRequest) -> HttpResponse:

    sales_xml = http_request.body["xml"]
    duepay_csv = http_request.body["csv"]

    dataframe_sales = SalesService().generate_sales_df_cpf_total_chave(sales_xml)
    dataframe_duepay = DuepayService().generate_duepay_df_total(duepay_csv) 

    report = self.__merge_dataframe_sales_and_duepay(dataframe_sales, dataframe_duepay)

    excel_report_buffer = self.__export_dataframe(report)

    formatted_response = self.__formatted_response(excel_report_buffer)

    return formatted_response

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