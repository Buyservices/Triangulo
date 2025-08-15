"""
Routers para endpoints do catálogo de consórcios.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.interfaces.http.api.v1.controllers_catalogo import (
    get_categorias,
    get_filiais,
    get_tipos_venda,
    get_bens_disponiveis,
    get_prazos_disponiveis,
    get_regra_cobranca,
)
from app.interfaces.http.api.v1.schemas_catalogo import (
    ListaTiposGruposSchema,
    ListaFiliaisSchema,
    ListaTiposVendasSchema,
    ListaBensDisponiveisSchema,
    ListaPrazosDisponiveisSchema,
    RegraCobrancaSchema,
)
from app.container import build_consultar_catalogo_uc
from app.application.use_cases.consultar_catalogo import ConsultarCatalogoUseCase

router = APIRouter(
    prefix="/catalog", 
    tags=["Catálogo de Consórcios"],
    responses={
        200: {"description": "Consulta realizada com sucesso"},
        400: {"description": "Parâmetros inválidos"},
        500: {"description": "Erro interno do servidor ou integração Newcon"}
    }
)


@router.get(
    "/categories", 
    response_model=ListaTiposGruposSchema,
    summary="Consultar Categorias de Consórcio",
    description="""
    **Consulta todas as categorias de consórcio disponíveis no sistema.**
    
    Este endpoint retorna a lista completa de categorias como Imóveis, Veículos, 
    Motocicletas, etc. que estão disponíveis para consórcio.
    
    **Características**:
    - ✅ **Sem parâmetros** - Consulta simples e direta
    - ✅ **Dados estáticos** - Raramente mudam, ideal para cache
    - ✅ **13 categorias** - Cobertura completa do sistema Newcon
    
    **Integração**: Chama o método `cnsTiposGrupos` do WebService SOAP da Newcon.
    **Cache**: Recomendado para dados que mudam raramente.
    
    **Exemplos de categorias**:
    - `IM` = IMOVEIS
    - `AI` = AUTOMOVEIS IMPORTADOS  
    - `MT` = MOTOCICLETAS
    - `EL` = ELETROELETRONICOS
    """
)
async def consultar_categorias(
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_categorias(uc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/filiais", 
    response_model=ListaFiliaisSchema,
    summary="Consultar Filiais de Venda",
    description="""
    **Consulta todas as filiais de venda cadastradas no sistema Newcon.**
    
    Este endpoint retorna a lista de filiais onde é possível realizar
    vendas de consórcio e consultar o catálogo de ofertas.
    
    **Características**:
    - ✅ **Sem parâmetros** - Consulta simples e direta
    - ✅ **Dados estáticos** - Raramente mudam, ideal para cache
    - ✅ **1 filial ativa** - TRIANGULO ADM. DE CONSORCIOS LTDA
    
    **Integração**: Chama o método `cnsFiliaisVendas` do WebService SOAP da Newcon.
    **Cache**: Recomendado para dados que mudam raramente.
    
    **Filiais disponíveis**:
    - `1` = TRIANGULO ADM. DE CONSORCIOS LTDA
    """
)
async def consultar_filiais(
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_filiais(uc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/sale-types", 
    response_model=ListaTiposVendasSchema,
    summary="Consultar Tipos de Venda por Categoria",
    description="""
    **Consulta os tipos de venda disponíveis para uma categoria específica.**
    
    Este endpoint retorna os tipos de comercialização (ex: Venda Direta, Consórcio)
    disponíveis para uma categoria como Imóveis, Veículos, etc.
    
    **Características**:
    - 🔍 **Filtro por categoria** - Especifique a categoria desejada
    - ⚠️ **Dados variáveis** - Nem todas as categorias possuem tipos de venda
    - 📊 **Integração real** - Dados vindos diretamente da base Newcon
    
    **Parâmetros**:
    - `tipo_grupo` (obrigatório): Código da categoria (ex: "IM" para Imóveis)
    
    **Integração**: Chama o método `cnsTiposVendas` do WebService SOAP da Newcon.
    
    **Exemplos de uso**:
    - `/sale-types?tipo_grupo=IM` → Tipos de venda para Imóveis
    - `/sale-types?tipo_grupo=AI` → Tipos de venda para Automóveis Importados
    
    **Nota**: Algumas categorias podem retornar lista vazia se não possuírem
    tipos de venda cadastrados no sistema.
    """
)
async def consultar_tipos_venda(
    tipo_grupo: str = Query(
        ..., 
        description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis Importados)",
        example="IM"
    ),
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_tipos_venda(tipo_grupo, uc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/items", 
    response_model=ListaBensDisponiveisSchema,
    summary="Consultar Bens (Cartas de Crédito) Disponíveis",
    description="""
    **Consulta os bens disponíveis para consórcio (cartas de crédito).**
    
    Este endpoint retorna a lista de bens disponíveis com seus valores e descrições
    para uma combinação específica de filial, categoria e tipo de venda.
    
    **Características**:
    - 💰 **Valores reais** - Preços das cartas de crédito em tempo real
    - 🏢 **Filtros específicos** - Filial + Categoria + Tipo de Venda
    - 📋 **Descrições detalhadas** - Nome completo de cada bem
    
    **Parâmetros obrigatórios**:
    - `filial`: Código da filial (ex: "1" = TRIANGULO ADM.)
    - `tipo_grupo`: Código da categoria (ex: "IM" = Imóveis)
    - `tipo_venda`: Código do tipo de venda (ex: "10", "20")
    
    **Integração**: Chama o método `cnsBensDisponiveis` do WebService SOAP da Newcon.
    
    **Exemplos de uso**:
    - `/items?filial=1&tipo_grupo=IM&tipo_venda=10` → Bens de Imóveis na filial 1
    - `/items?filial=1&tipo_grupo=AI&tipo_venda=20` → Bens de Automóveis Importados
    
    **Resultado**: Lista de cartas de crédito com valores para montar a vitrine.
    """
)
async def consultar_bens_disponiveis(
    filial: str = Query(
        ..., 
        description="Código da filial (ex: 1=TRIANGULO ADM.)",
        example="1"
    ),
    tipo_grupo: str = Query(
        ..., 
        description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis)",
        example="IM"
    ),
    tipo_venda: str = Query(
        ..., 
        description="Código do tipo de venda (ex: 10, 20, 30)",
        example="10"
    ),
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_bens_disponiveis(filial, tipo_grupo, tipo_venda, uc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/options", 
    response_model=ListaPrazosDisponiveisSchema,
    summary="Consultar Opções Comerciais (Prazos e Prestações)",
    description="""
    **Consulta as opções comerciais disponíveis para financiamento.**
    
    Este endpoint retorna as opções de financiamento incluindo prazos, valores de
    prestação, planos e informações sobre assembleias e cotas vagas.
    
    **Características**:
    - ⏰ **Prazos flexíveis** - Múltiplas opções de prazo disponíveis
    - 💰 **Prestações calculadas** - Valores de prestação em tempo real
    - 📅 **Assembleias** - Datas de próxima assembleia e vencimento
    - 🎯 **Filtros avançados** - Múltiplos parâmetros para consulta específica
    
    **Parâmetros obrigatórios**:
    - `unidade`: Código da unidade administrativa
    - `tipo_grupo`: Código da categoria (ex: "IM" = Imóveis)
    - `representante`: Código do representante comercial
    - `filial`: Código da filial (ex: "1" = TRIANGULO ADM.)
    
    **Parâmetros opcionais**:
    - `situacao_grupo`: A=Ativo, F=Fechado, X=Cancelado
    - `pessoa`: F=Física, J=Jurídica
    - `ordem_pesquisa`: G=Grupo, P=Prazo
    - `tipo_venda`: Código do tipo de venda
    - `bem`: Código do bem específico
    - `prazo`: Prazo em meses
    - `dia_vencimento`: Dia do vencimento (1-31)
    - `data_assembleia`: Data da assembleia (YYYY-MM-DD)
    - `codigo_grupo`: Código do grupo específico
    - `rateia`: S=Sim, N=Não
    
    **Integração**: Chama o método `cnsPrazosDisponiveis` do WebService SOAP da Newcon.
    
    **Exemplos de uso**:
    - `/options?unidade=001&tipo_grupo=IM&representante=000001&filial=1&pessoa=F&situacao_grupo=A&rateia=N`
    
    **Resultado**: Opções comerciais completas para montar a vitrine de financiamento.
    """
)
async def consultar_opcoes_comerciais(
    unidade: str = Query(
        ..., 
        description="Código da unidade administrativa",
        example="001"
    ),
    tipo_grupo: str = Query(
        ..., 
        description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis)",
        example="IM"
    ),
    representante: str = Query(
        ..., 
        description="Código do representante comercial",
        example="000001"
    ),
    filial: str = Query(
        ..., 
        description="Código da filial (ex: 1=TRIANGULO ADM.)",
        example="1"
    ),
    situacao_grupo: str = Query(
        default="A", 
        description="Situação do grupo (A=Ativo, F=Fechado, X=Cancelado)",
        example="A"
    ),
    pessoa: str = Query(
        default="F", 
        description="Tipo de pessoa (F=Física, J=Jurídica)",
        example="F"
    ),
    ordem_pesquisa: str = Query(
        default="G", 
        description="Ordem de pesquisa (G=Grupo, P=Prazo)",
        example="G"
    ),
    tipo_venda: str = Query(None, description="Código do tipo de venda", example="10"),
    bem: str = Query(None, description="Código do bem específico", example="123"),
    prazo: int = Query(None, description="Prazo em meses", example=120),
    dia_vencimento: int = Query(None, description="Dia do vencimento (1-31)", example=15),
    data_assembleia: str = Query(None, description="Data da assembleia (YYYY-MM-DD)", example="2024-12-01"),
    codigo_grupo: str = Query(None, description="Código do grupo específico", example="456"),
    rateia: str = Query(default="N", description="Se rateia (S=Sim, N=Não)", example="N"),
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_prazos_disponiveis(
            unidade=unidade,
            tipo_grupo=tipo_grupo,
            representante=representante,
            filial=filial,
            situacao_grupo=situacao_grupo,
            pessoa=pessoa,
            ordem_pesquisa=ordem_pesquisa,
            tipo_venda=tipo_venda,
            bem=bem,
            prazo=prazo,
            dia_vencimento=dia_vencimento,
            data_assembleia=data_assembleia,
            codigo_grupo=codigo_grupo,
            rateia=rateia,
            uc=uc,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/rules", 
    response_model=RegraCobrancaSchema,
    summary="Consultar Regras de Cobrança (Composição das Parcelas)",
    description="""
    **Consulta a composição detalhada das parcelas de um plano específico.**
    
    Este endpoint retorna o breakdown financeiro completo incluindo percentuais
    de taxa administrativa, fundo de reserva, seguros e valor calculado por faixa.
    
    **Características**:
    - 💰 **Breakdown financeiro** - Composição detalhada de cada parcela
    - 📊 **Percentuais precisos** - Taxa adm, fundo reserva, seguros
    - 🎯 **Cálculo por faixa** - Valores específicos para cada faixa de parcelas
    - 🔍 **Parâmetros específicos** - Todos os campos são obrigatórios para precisão
    
    **Parâmetros obrigatórios**:
    - `plano`: Código do plano de consórcio
    - `tipo_venda`: Código do tipo de venda (ex: "10", "20")
    - `bem`: Código do bem específico
    - `tipo_grupo`: Código da categoria (ex: "IM" = Imóveis)
    - `filial`: Código da filial (ex: "1" = TRIANGULO ADM.)
    - `rateia`: S=Sim, N=Não
    - `numero_assembleia_emissao`: Número da assembleia de emissão
    - `prazo`: Prazo em meses (ex: 60, 120, 180)
    - `sequencia_agrupamento`: Sequência de agrupamento
    
    **Integração**: Chama o método `cnsRegraCobranca` do WebService SOAP da Newcon.
    
    **Exemplos de uso**:
    - `/rules?plano=7&tipo_venda=10&bem=123&tipo_grupo=IM&filial=1&rateia=N&numero_assembleia_emissao=45&prazo=120&sequencia_agrupamento=456`
    
    **Resultado**: Composição financeira detalhada para simulação precisa de financiamento.
    """
)
async def consultar_regra_cobranca(
    plano: str = Query(
        ..., 
        description="Código do plano de consórcio",
        example="7"
    ),
    tipo_venda: str = Query(
        ..., 
        description="Código do tipo de venda (ex: 10, 20)",
        example="10"
    ),
    bem: str = Query(
        ..., 
        description="Código do bem específico",
        example="123"
    ),
    tipo_grupo: str = Query(
        ..., 
        description="Código do tipo de grupo (ex: IM=Imóveis)",
        example="IM"
    ),
    filial: str = Query(
        ..., 
        description="Código da filial (ex: 1=TRIANGULO ADM.)",
        example="1"
    ),
    rateia: str = Query(
        ..., 
        description="Se rateia (S=Sim, N=Não)",
        example="N"
    ),
    numero_assembleia_emissao: str = Query(
        ..., 
        description="Número da assembleia de emissão",
        example="45"
    ),
    prazo: int = Query(
        ..., 
        description="Prazo em meses (ex: 60, 120, 180)",
        example=120
    ),
    sequencia_agrupamento: str = Query(
        ..., 
        description="Sequência de agrupamento",
        example="456"
    ),
    uc: ConsultarCatalogoUseCase = Depends(build_consultar_catalogo_uc),
):
    try:
        return await get_regra_cobranca(
            plano=plano,
            tipo_venda=tipo_venda,
            bem=bem,
            tipo_grupo=tipo_grupo,
            filial=filial,
            rateia=rateia,
            numero_assembleia_emissao=numero_assembleia_emissao,
            prazo=prazo,
            sequencia_agrupamento=sequencia_agrupamento,
            uc=uc,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
