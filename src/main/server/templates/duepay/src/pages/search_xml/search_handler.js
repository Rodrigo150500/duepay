import {DuepaySearchXMLService} from "./service/duepay_search_xml_service.js"
import {search_xml_view} from "./view/search_xml_view.js";

class DuepaySearchXMLHandler{

    search_xml(){

        const btn_search = document.getElementById("btn-search-xml")
        btn_search.addEventListener("click", async () => {

            const service = new DuepaySearchXMLService()
            const response = await service.search()

            search_xml_view.show_to_interface(response)

            
        })

 
    }

}

const duepay_search_xml_handler = new DuepaySearchXMLHandler()
duepay_search_xml_handler.search_xml()