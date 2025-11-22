from io import BytesIO
from src.main.http_types.http_request.http_request import HttpRequest
from src.main.http_types.http_response.http_response import HttpResponse
from src.utils.unzip_file import unzip_file
from xml.etree import ElementTree as ET
from .interface.search_xml_use_case_inteface import SearchForXMLInterface
from src.validations.mime_type_validation.mime_type_validation import mime_type_validation
from src.errors.types.http_bad_request import HttpBadRequest
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntity


class SearchForXML(SearchForXMLInterface):

    def __init__(self)-> None:
       self.__found = False

    def search(self, http_request: HttpRequest) -> HttpResponse:

        try:

            xml_zipped = http_request.body["xml"]

            if mime_type_validation(xml_zipped) == False: raise HttpBadRequest("Erro: verifique os arquivos enviados")

            value_cpf_or_total = http_request.body["value"]

            if not value_cpf_or_total: raise HttpBadRequest("Erro: Verifique os valores de Total/CPF")

            cpf_or_total = self.__verify_if_value_is_cpf_or_total(value_cpf_or_total)

            xml_list = unzip_file(xml_zipped)

            data = self.__search_manager(xml_list, cpf_or_total)
            
            response = self.__formatted_response(data, self.__found)
            
            return response

        except Exception as exception:

            print(f"Error: {str(exception)}")

            raise HttpUnprocessableEntity("Erro interno ao processar os arquivos. Verifique os XMLs enviados.")
        
    
    def __search_manager(self, xml_list: list, value) -> list:
        
        xml_found_list = []
        count = 0
        for xml in xml_list:
            count+=1
            tree = ET.parse(BytesIO(xml))
            root = tree.getroot()            

            #pegando a data
            date_reference = root[0][0][0][6]
            
            date_value = date_reference.text.strip()

            date = self.__format_date(date_value)
            
            #Pegando a chave da Nota
            nfe_reference = root[0][0]

            id_value = nfe_reference.get("Id")

            nfe = self.__format_nfe(id_value)

            #Pegando o valor total
            total_reference = float(root[0][0][-4][0][-1].text)
            
            cpf_root = root[0][0][2][0]

            cpf_reference = cpf_root.text

            cpf = None
            
            if cpf_reference is not None:
                cpf_value = cpf_reference.strip()  
                cpf = self.__format_cpf(cpf_value)  # Agora formatado corretamente como xxx.xxx.xxx-xx

          
            if (isinstance(value, str) and cpf == value) or (isinstance(value, float) and total_reference == value):  # Se for CPF (string)
                data = {
                    # "name": xml,
                    "data": date,
                    "cpf": cpf if cpf is not None else "Sem CPF",
                    "total": total_reference,
                    "nfe": nfe
                }
                xml_found_list.append(data)
                self.__found = True
            

        if self.__found == False:
            data = {
                "name": "Não encontrado",
                "data": "Não encontrado",
                "cpf": "Não encontrado",
                "total": "Não encontrado",
                "nfe": "Não encontrado"
            }
            xml_found_list.append(data)

            return xml_found_list
        
        return xml_found_list

            
    def __format_nfe(self, nfe_value: str) -> str:

        nfe_with_no_string = nfe_value[3:]

        nfe = ""
        for i in range(0, len(nfe_with_no_string)):
            if i % 4 == 0:
                nfe += " "+nfe_with_no_string[i]
            else:
                nfe += nfe_with_no_string[i]

        return nfe
    
    
    def __format_cpf(self, cpf_value: str) -> str:
        #xxx.xxx.xxx-xx
        cpf = f"{cpf_value[0:3]}.{cpf_value[3:6]}.{cpf_value[6:9]}-{cpf_value[9:11]}"
        return cpf
    

    def __format_date(self, date: str) -> str:

        #dd/mm/aaaa
        #20250203 03/02/2025 

        dia = date[8:10]
        mes = date[5:7]
        ano = date[0:4]

        date_formated = f'{dia}/{mes}/{ano}'

        return date_formated
    
    
    def __formatted_response(self, data: list, isFound: bool) -> HttpResponse:
        return HttpResponse(
            body={
                "found": isFound,
                "data": data
            },
            status_code=200
        )
    
    
    def __verify_if_value_is_cpf_or_total(self, value: str) -> bool:
        # Verifica se o valor é um CPF ou um total
        if isinstance(value, str) and len(value) == 14:
            value = str(value)
        else:
            value = float(value)

        return value