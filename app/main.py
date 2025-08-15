from fastapi import FastAPI
from app.interfaces.http.api.v1.routers import router as v1_router
from app.interfaces.http.api.v1.routers_catalogo import router as catalogo_router


app = FastAPI(
    title="API Newcon Consórcio - Bridge de Integração",
    version="2.0.0",
    description="""
    ## 🚀 **API de Integração com Sistema Newcon Consórcio**
    
    Esta API serve como **bridge** entre sistemas externos e o sistema **Newcon Consórcio**,
    expondo endpoints REST que internamente se comunicam com WebServices SOAP da Newcon.
    
    ### 🎯 **Funcionalidades Implementadas**
    
    #### ✅ **Registro de Clientes** (FASE 1 - CONCLUÍDA)
    - **Endpoint**: `POST /v1/clientes`
    - **Status**: ✅ **FUNCIONANDO** - Integração completa e testada
    - **Integração**: Chama `prcManutencaoCliente_new` da Newcon
    
                    #### ✅ **Catálogo de Consórcios** (FASE 2 - CONCLUÍDA)
                - **Status**: 🎉 **100% FUNCIONANDO** + ✅ **TESTADO EXAUSTIVAMENTE**
                - **Endpoints**: 6 endpoints para consulta de catálogo
                - **Integração**: WebServices SOAP da Newcon (métodos `cns*`) ✅ **100% FUNCIONANDO**
                - **Dados**: 13 categorias + 1 filial + 157 tipos de venda retornados
    
    ### 🏗️ **Arquitetura**
    
    - **DDD + Clean Architecture**: Separação clara de responsabilidades
    - **Anti-Corruption Layer**: Mappers/parsers isolam a API da estrutura SOAP
    - **Async/Await**: Operações não-bloqueantes para melhor performance
    - **Pydantic**: Validação robusta de dados e schemas
    
    ### 🔗 **Integração Newcon**
    
    - **WebServices SOAP**: Comunicação via métodos `cns*` (consulta) e `prc*` (processo)
    - **Protocolo**: HTTP POST com envelope SOAP XML
    - **Timeout**: 30 segundos configurável
    - **Tratamento de Erros**: Captura e reporta erros específicos da Newcon
    
    ### 📚 **Documentação**
    
    - **Swagger UI**: `/docs` - Interface interativa completa
    - **Testes**: `TESTES_CATALOGO_OFERTAS.md` - Guia passo a passo
    - **README**: Visão geral do projeto e roadmap
    
                    ### 🧪 **Como Testar**
                
                1. **Iniciar API**: `uvicorn app.main:app --reload --port 8000`
                2. **Swagger UI**: `http://localhost:8000/docs`
                3. **Testes Completos**: Todos os endpoints testados e funcionando ✅
                4. **Dados Reais**: 13 categorias + 1 filial + 157 tipos de venda ✅
    
    ---
    
    **Desenvolvido com FastAPI + Python**
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(v1_router, prefix="/v1")
app.include_router(catalogo_router, prefix="/v1")

