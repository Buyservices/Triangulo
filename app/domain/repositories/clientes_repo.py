from typing import Protocol
from app.application.dto.cliente_dto import ClienteInDTO, ClienteOutDTO

class ClientesRepository(Protocol):
    async def registrar_cliente(self, dto: ClienteInDTO) -> ClienteOutDTO: ...
