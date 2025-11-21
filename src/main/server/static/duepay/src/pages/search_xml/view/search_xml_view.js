class SearchXMLView{

    show_to_interface(xml_found){

        console.log("XML encontrado:", xml_found);

        const isFound = xml_found["found"]

        if (!isFound) {
            document.getElementById("resultado").value = "Nada encontrado";
        }else{

            let response = ""

            for(let i = 0; i < xml_found["data"].length; i++) {
                response += `CPF: ${xml_found["data"][i]["cpf"]}\nTotal: ${xml_found["data"][i]["total"]}\nChave: ${xml_found["data"][i]["nfe"]}\nData: ${xml_found["data"][i]["data"]}\n\n`;
                
            }
            document.getElementById("resultado").value = response;
        }




    }
}

export const search_xml_view = new SearchXMLView();