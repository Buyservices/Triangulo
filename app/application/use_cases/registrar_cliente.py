"""
Módulo contendo o caso de uso para registro de clientes.
"""
from app.domain.entities import Cliente


class RegistrarClienteUseCase:
    """
    Caso de uso responsável por registrar um cliente na Newcon.
    """

    def __init__(self, repo):
        self.repo = repo

    def execute(self, cliente_dto) -> dict:
        """
        Valida os dados, cria a entidade Cliente e envia para o repositório.
        """
        # Converte o DTO para dicionário se for um objeto Pydantic
        if hasattr(cliente_dto, 'dict'):
            cliente_data = cliente_dto.dict()
        elif hasattr(cliente_dto, 'model_dump'):
            cliente_data = cliente_dto.model_dump()
        else:
            cliente_data = cliente_dto
            
        cliente = Cliente(**cliente_data)  # validação via Pydantic
        
        # Converte a entidade para dicionário
        if hasattr(cliente, 'dict'):
            cliente_dict = cliente.dict()
        elif hasattr(cliente, 'model_dump'):
            cliente_dict = cliente.model_dump()
        else:
            cliente_dict = cliente
            
        result = self.repo.registrar_cliente(cliente_dict)
        return result if isinstance(result, dict) else {"sucesso": True, "mensagem": "Cliente registrado com sucesso", "bruto_xml": str(result)}
