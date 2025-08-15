"""
Schemas Pydantic para a API de catálogo de consórcios.
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal


# Schemas de entrada (Query Parameters)
class ConsultaTiposVendasSchema(BaseModel):
    tipo_grupo: str = Field(
        ..., 
        description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis Importados, MT=Motocicletas)",
        example="IM"
    )


class ConsultaBensDisponiveisSchema(BaseModel):
    filial: str = Field(..., description="Código da filial (ex: 1=TRIANGULO ADM. DE CONSORCIOS)", example="1")
    tipo_grupo: str = Field(..., description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis)", example="IM")
    tipo_venda: str = Field(..., description="Código do tipo de venda (ex: 10, 20, etc.)", example="10")


class ConsultaPrazosDisponiveisSchema(BaseModel):
    unidade: str = Field(..., description="Código da unidade administrativa", example="001")
    tipo_grupo: str = Field(..., description="Código do tipo de grupo (ex: IM=Imóveis, AI=Automóveis)", example="IM")
    representante: str = Field(..., description="Código do representante comercial", example="000001")
    situacao_grupo: str = Field(default="A", description="Situação do grupo (A=Ativo, F=Fechado, X=Cancelado)", example="A")
    pessoa: str = Field(default="F", description="Tipo de pessoa (F=Física, J=Jurídica)", example="F")
    ordem_pesquisa: str = Field(default="G", description="Ordem de pesquisa (G=Grupo, P=Prazo)", example="G")
    filial: str = Field(..., description="Código da filial (ex: 1=TRIANGULO ADM.)", example="1")
    tipo_venda: Optional[str] = Field(None, description="Código do tipo de venda (ex: 10, 20)", example="10")
    bem: Optional[str] = Field(None, description="Código do bem específico", example="123")
    prazo: Optional[int] = Field(None, description="Prazo em meses (ex: 60, 120, 180)", example=120)
    dia_vencimento: Optional[int] = Field(None, description="Dia do vencimento (1-31)", example=15)
    data_assembleia: Optional[str] = Field(None, description="Data da assembleia (YYYY-MM-DD)", example="2024-12-01")
    codigo_grupo: Optional[str] = Field(None, description="Código do grupo específico", example="456")
    rateia: Optional[str] = Field(default="N", description="Se rateia (S=Sim, N=Não)", example="N")


class ConsultaRegraCobrancaSchema(BaseModel):
    plano: str = Field(..., description="Código do plano de consórcio", example="7")
    tipo_venda: str = Field(..., description="Código do tipo de venda (ex: 10, 20)", example="10")
    bem: str = Field(..., description="Código do bem específico", example="123")
    tipo_grupo: str = Field(..., description="Código do tipo de grupo (ex: IM=Imóveis)", example="IM")
    filial: str = Field(..., description="Código da filial (ex: 1=TRIANGULO ADM.)", example="1")
    rateia: str = Field(..., description="Se rateia (S=Sim, N=Não)", example="N")
    numero_assembleia_emissao: str = Field(..., description="Número da assembleia de emissão", example="45")
    prazo: int = Field(..., description="Prazo em meses (ex: 60, 120, 180)", example=120)
    sequencia_agrupamento: str = Field(..., description="Sequência de agrupamento", example="456")


# Schemas de saída
class TipoGrupoSchema(BaseModel):
    codigo: str = Field(..., description="Código único do tipo de grupo (ex: IM, AI, MT)")
    descricao: str = Field(..., description="Nome descritivo do tipo de grupo (ex: IMOVEIS, AUTOMOVEIS IMPORTADOS)")


class FilialVendaSchema(BaseModel):
    codigo: str = Field(..., description="Código único da filial (ex: 1)")
    nome: str = Field(..., description="Nome completo da filial (ex: TRIANGULO ADM. DE CONSORCIOS LTDA)")


class TipoVendaSchema(BaseModel):
    codigo: str = Field(..., description="Código único do tipo de venda (ex: 10, 20, 30)")
    descricao: str = Field(..., description="Descrição do tipo de venda (ex: VENDA DIRETA, CONSORCIO)")


class BemDisponivelSchema(BaseModel):
    codigo: str = Field(..., description="Código único do bem disponível")
    descricao: str = Field(..., description="Descrição detalhada do bem (ex: CASA RESIDENCIAL, APARTAMENTO)")
    valor: Decimal = Field(..., description="Valor monetário do bem em reais (R$)")


class BemDisponivelPorGrupoSchema(BaseModel):
    codigo_grupo: str = Field(..., description="Código do grupo")
    codigo_bem: str = Field(..., description="Código do bem")
    descricao: str = Field(..., description="Descrição do bem")
    valor: Decimal = Field(..., description="Valor do bem")


class PrazoDisponivelSchema(BaseModel):
    codigo_grupo: str = Field(..., description="Código do grupo")
    prazo_venda: Optional[int] = Field(None, description="Prazo de venda em meses")
    prazo_grupo: Optional[int] = Field(None, description="Prazo do grupo em meses")
    dia_vencimento: Optional[int] = Field(None, description="Dia do vencimento")
    valor_prestacao: Optional[Decimal] = Field(None, description="Valor da prestação")
    codigo_bem: str = Field(..., description="Código do bem")
    valor_bem: Decimal = Field(..., description="Valor do bem")
    codigo_plano: str = Field(..., description="Código do plano")
    sequencia_agrupamento: str = Field(..., description="Sequência de agrupamento")
    percentual_taxa_adm: Optional[Decimal] = Field(None, description="Percentual da taxa administrativa")
    percentual_fundo_reserva: Optional[Decimal] = Field(None, description="Percentual do fundo de reserva")
    percentual_mensal: Optional[Decimal] = Field(None, description="Percentual mensal")
    data_proxima_assembleia: Optional[str] = Field(None, description="Data da próxima assembleia")
    cotas_vagas: Optional[int] = Field(None, description="Quantidade de cotas vagas")
    data_vencimento_limite: Optional[str] = Field(None, description="Data limite de vencimento")


class FaixaParcelaSchema(BaseModel):
    faixa_inicial: int = Field(..., description="Faixa inicial de parcelas")
    faixa_final: int = Field(..., description="Faixa final de parcelas")
    percentual_fundo_comum: Decimal = Field(..., description="Percentual do fundo comum")
    percentual_taxa_adm: Decimal = Field(..., description="Percentual da taxa administrativa")
    percentual_fundo_reserva: Decimal = Field(..., description="Percentual do fundo de reserva")
    percentual_seguros: Optional[Decimal] = Field(None, description="Percentual de seguros")
    valor_parcela: Decimal = Field(..., description="Valor da parcela")


class RegraCobrancaSchema(BaseModel):
    codigo_plano: str = Field(..., description="Código do plano")
    prazo: int = Field(..., description="Prazo em meses")
    sequencia_agrupamento: str = Field(..., description="Sequência de agrupamento")
    faixas_parcelas: List[FaixaParcelaSchema] = Field(..., description="Faixas de parcelas")


# Schemas de resposta da API
class CatalogoResponseSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    dados: Optional[dict] = Field(None, description="Dados retornados pela operação")
    erro: Optional[str] = Field(None, description="Descrição do erro, se houver")


# Schemas de listagem
class ListaTiposGruposSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    categorias: List[TipoGrupoSchema] = Field(..., description="Lista de categorias disponíveis")


class ListaFiliaisSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    filiais: List[FilialVendaSchema] = Field(..., description="Lista de filiais disponíveis")


class ListaTiposVendasSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    tipos_venda: List[TipoVendaSchema] = Field(..., description="Lista de tipos de venda disponíveis")


class ListaBensDisponiveisSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    bens: List[BemDisponivelSchema] = Field(..., description="Lista de bens disponíveis")


class ListaPrazosDisponiveisSchema(BaseModel):
    sucesso: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    prazos: List[PrazoDisponivelSchema] = Field(..., description="Lista de prazos disponíveis")
