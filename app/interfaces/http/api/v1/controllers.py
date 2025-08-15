from app.interfaces.http.api.v1.schemas import ClienteInSchema, ClienteOutSchema
from app.application.use_cases.registrar_cliente import RegistrarClienteUseCase

async def post_registrar_cliente(body: ClienteInSchema, uc: RegistrarClienteUseCase) -> ClienteOutSchema:
    result = uc.execute(body)
    
    # Converte o resultado para dicionário se necessário
    if hasattr(result, 'dict'):
        result_dict = result.dict()
    elif hasattr(result, 'model_dump'):
        result_dict = result.model_dump()
    else:
        result_dict = result
        
    return ClienteOutSchema(**result_dict)
