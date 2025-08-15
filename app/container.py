"""
Módulo de configuração de dependências da aplicação.
"""
from app.application.use_cases.registrar_cliente import RegistrarClienteUseCase
from app.infrastructure.repositories.clientes_repo_newcon_new import ClientesRepositoryNewconNew


def build_registrar_cliente_uc():
    """
    Configura as dependências e devolve uma instância do caso de uso
    RegistrarClienteUseCase com o repositório já injetado.
    """
    # Se quisermos trocar o cliente HTTP futuramente, basta passar aqui
    http_client = None  # None = usa requests nativo
    repo = ClientesRepositoryNewconNew(http_client=http_client)

    return RegistrarClienteUseCase(repo)
