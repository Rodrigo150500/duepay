import { CONFIG } from "../../../../../../config/config.js";

export class DuepayRespository{

    async get_search_xml(formData){

        const response = await fetch(`${CONFIG["API_URL"]}/duepay_search_xml`, {
            method: "POST",
            body:formData
        });

        const response_json = await response.json();
        
        return response_json;
    }
}