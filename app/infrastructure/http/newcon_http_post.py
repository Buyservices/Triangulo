import httpx
from urllib.parse import urlencode

class NewconHttpPostClient:
    """
    POST form-url-encoded para operações *_new, e.g. .../wsRegVenda.asmx/prcManutencaoCliente_new
    """
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def post_form(self, operation: str, data: dict[str, str | int | float | None]) -> tuple[int, str]:
        payload = {k: str(v) for k, v in data.items() if v is not None}
        url = f"{self.base_url}/{operation}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, content=urlencode(payload), headers=headers)
            # NÃO dar raise aqui; devolver status e corpo para o repo decidir.
            return resp.status_code, resp.text
