from fastapi import APIRouter, Depends, HTTPException
from app.interfaces.http.api.v1.controllers import post_registrar_cliente
from app.interfaces.http.api.v1.schemas import ClienteInSchema, ClienteOutSchema
from app.container import build_registrar_cliente_uc
from app.application.use_cases.registrar_cliente import RegistrarClienteUseCase

router = APIRouter(tags=["clientes"])


@router.post("/clientes", response_model=ClienteOutSchema)
async def registrar_cliente(
    body: ClienteInSchema,
    uc: RegistrarClienteUseCase = Depends(build_registrar_cliente_uc),
):
    try:
        return await post_registrar_cliente(body, uc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
