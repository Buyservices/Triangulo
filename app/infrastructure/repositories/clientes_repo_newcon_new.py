import requests
from typing import Any
from app.infrastructure.http.mappers_new import map_cliente_to_form


class ClientesRepositoryNewconNew:
    """
    Repositório responsável por enviar requisições HTTP para a Newcon
    usando o endpoint `prcManutencaoCliente_new`.
    """

    def __init__(self, http_client: Any = None):
        # Permite injetar http_client (para testes ou requests mockados).
        # Caso não seja passado, usa o requests nativo.
        self.http_client = http_client or requests

    def registrar_cliente(self, cliente_dto: dict) -> dict:
        """
        Recebe DTO de cliente, transforma no payload esperado
        e envia via POST para a API da Newcon.
        """
        url = (
            "https://webatendimento.consorciotriangulo.com.br/"
            "wsregvenda/wsRegVenda.asmx/prcManutencaoCliente_new"
        )

        form = map_cliente_to_form(cliente_dto)

        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/xml, application/xml'
            }
            

            
            response = self.http_client.post(url, data=form, headers=headers, timeout=30)
            response.raise_for_status()
            return {
                "sucesso": True,
                "mensagem": "Cliente registrado com sucesso",
                "bruto_xml": response.text,
            }
        except requests.RequestException as e:
            return {
                "sucesso": False,
                "mensagem": (
                    f"HTTP {getattr(e.response, 'status_code', 'erro')} do provedor | "
                    f"body: {getattr(e.response, 'text', str(e))}"
                ),
                "bruto_xml": getattr(e.response, "text", str(e)),
            }
