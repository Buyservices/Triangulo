"""
Cliente SOAP para integração com WebServices da Newcon.
"""

import httpx
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from defusedxml import ElementTree


class NewconSoapClient:
    """
    Cliente SOAP para WebServices da Newcon.
    Suporta métodos cns* (consulta) e prc* (processo).
    """

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _build_soap_envelope(self, method: str, params: Dict[str, Any]) -> str:
        """Constrói envelope SOAP para o método especificado"""

        # Constrói o corpo SOAP
        body_params = ""
        for key, value in params.items():
            if value is not None:
                body_params += f"<{key}>{value}</{key}>"

        soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <{method} xmlns="http://www.cnpm.com.br/">
      {body_params}
    </{method}>
  </soap:Body>
</soap:Envelope>"""

        return soap_envelope

    async def call_soap_method(
        self, method: str, params: Dict[str, Any], service: str = "wsRegVenda"
    ) -> tuple[int, str]:
        """
        Chama método SOAP da Newcon.

        Args:
            method: Nome do método SOAP (ex: cnsTiposGrupos)
            params: Parâmetros do método
            service: Serviço SOAP (wsRegVenda, ws_atendimento, ws_autorizador)

        Returns:
            Tuple (status_code, response_text)
        """

        # Constrói URL do serviço
        if service == "wsRegVenda":
            url = urljoin(self.base_url, "wsregvenda/wsRegVenda.asmx")
        elif service == "ws_atendimento":
            url = urljoin(self.base_url, "wsregvenda/ws_atendimento.asmx")
        elif service == "ws_autorizador":
            url = urljoin(self.base_url, "wsregvenda/ws_autorizador.asmx")
        else:
            url = urljoin(self.base_url, f"wsregvenda/{service}.asmx")

        # Constrói envelope SOAP
        soap_body = self._build_soap_envelope(method, params)

        # Headers para SOAP
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"http://www.cnpm.com.br/{method}",
            "Accept": "text/xml, application/xml",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, content=soap_body, headers=headers)
                return response.status_code, response.text

        except Exception as e:
            return 500, f"Erro na chamada SOAP: {str(e)}"

    def parse_soap_response(self, xml_response: str) -> Dict[str, Any]:
        """
        Faz parse da resposta SOAP da Newcon.

        Args:
            xml_response: Resposta XML do WebService

        Returns:
            Dicionário com dados parseados
        """
        try:
            # Remove namespace para facilitar parsing
            xml_response = xml_response.replace('xmlns="http://www.cnpm.com.br/"', "")

            root = ElementTree.fromstring(xml_response)

            # Procura por elementos de dados
            result = {}

            # Procura por DataSet (estrutura comum da Newcon)
            dataset = root.find(".//DataSet")
            if dataset is not None:
                # Parse de DataSet
                tables = dataset.findall(".//Table")
                for table in tables:
                    table_name = table.get("name", "Table")
                    rows = []

                    for row in table.findall(".//Row"):
                        row_data = {}
                        for col in row.findall(".//Column"):
                            col_name = col.get("name", "")
                            col_value = col.text or ""
                            row_data[col_name] = col_value
                        rows.append(row_data)

                    result[table_name] = rows

            # Procura por NewDataSet dentro de diffgram (estrutura real da Newcon)
            if not result:
                new_dataset = root.find(".//NewDataSet")
                if new_dataset is not None:
                    tables = new_dataset.findall(".//Table")
                    if tables:
                        rows = []
                        for table in tables:
                            row_data = {}
                            for child in table:
                                if child.tag.startswith('{'):
                                    # Remove namespace do tag
                                    tag_name = child.tag.split('}', 1)[1]
                                else:
                                    tag_name = child.tag
                                row_data[tag_name] = child.text or ""
                            rows.append(row_data)
                        result["Table"] = rows

            # Procura por elementos diretos (para métodos simples)
            if not result:
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        result[elem.tag] = elem.text.strip()

            return result

        except Exception as e:
            return {"error": f"Erro no parse XML: {str(e)}", "raw": xml_response}

    def check_error_response(self, xml_response: str) -> Optional[str]:
        """
        Verifica se a resposta contém erro da Newcon.

        Args:
            xml_response: Resposta XML do WebService

        Returns:
            Mensagem de erro se houver, None caso contrário
        """
        try:
            # Procura por padrões de erro comuns da Newcon
            error_patterns = [
                "ErrMsg",
                "Parâmetro ausente",
                "Não é possível converter",
                "System.",
                "Erro",
            ]

            for pattern in error_patterns:
                if pattern.lower() in xml_response.lower():
                    # Extrai mensagem de erro específica
                    if "ErrMsg" in xml_response:
                        # Procura pela mensagem de erro específica
                        start = xml_response.find("<ErrMsg>")
                        if start != -1:
                            end = xml_response.find("</ErrMsg>", start)
                            if end != -1:
                                return xml_response[start + 8 : end]

                    # Retorna contexto do erro
                    lines = xml_response.split("\n")
                    for line in lines:
                        if any(
                            pattern.lower() in line.lower()
                            for pattern in error_patterns
                        ):
                            return line.strip()

                    return f"Erro detectado: {pattern}"

            return None

        except Exception:
            return None
