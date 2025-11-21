from io import BytesIO, StringIO
from xml.etree import ElementTree as ET
from pandas import DataFrame
from src.utils.unzip_file import unzip_file
from .interface.sales_service_interface import SalesServiceInterface

class SalesService(SalesServiceInterface):
    def generate_sales_df_cpf_total_chave(self, xml_zip) -> DataFrame:
        
        xml_unzipped_list = unzip_file(xml_zip)
        
        data_extracted_dict = self.__extract_cpf_total_chave_from_xml(xml_unzipped_list)

        dataframe_sales = DataFrame(data_extracted_dict)

        return dataframe_sales

    def __extract_cpf_total_chave_from_xml(self, xml_file) -> dict:
        
        data = {
            "Data": [],
            "CPF": [],
            "Total":[],
            "NFe": []
        }


        for xml in xml_file:      


            tree = ET.parse(BytesIO(xml))
            root = tree.getroot()
            
            # Etapa 1: pegar a tag NFe
            # for i in root[0][0]:
            #     print(i)
            # print(root[0][0][-4])
            # return

            cpf_root = root[0][0][2][0]

            if cpf_root.tag[-3::] != "CPF": continue

            cpf_reference = cpf_root.text

            if cpf_reference is not None:
                
                #Pegando CPF
                cpf_value = cpf_reference.strip()  

                cpf = self.__format_cpf(cpf_value)
                
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

                #Adicionando valores
                data["CPF"].append(cpf)
                data["NFe"].append(nfe)
                data["Total"].append(total_reference)
                data['Data'].append(date)
        
        return data
    
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
        #2025-10-29T13:41:52-03:00

        dia = date[8:10]
        mes = date[5:7]
        ano = date[0:4]

        date_formated = f'{dia}/{mes}/{ano}'


        return date_formated

