import { DuepayRespository } from "../model/repository/duepay_repository.js";

export class DuepaySearchXMLService {

    async search() {
        return new Promise((resolve, reject) => {
            document.getElementById("search_form").addEventListener("submit", async (event) => {
                event.preventDefault();

                const formData = new FormData(event.target);

                try {
                    const repository = new DuepayRespository();
                    const response = await repository.get_search_xml(formData);

                    resolve(response); // agora envia para quem chamou search()
                } catch (error) {
                    console.log("Erro ao enviar o formulário:", error);
                    reject(error);
                }
            }, { once: true }); // garante que escuta só 1 vez
        });
    }

}
