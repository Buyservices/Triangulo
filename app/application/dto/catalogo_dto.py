from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal


# DTOs de entrada para consultas
class ConsultaTiposVendasDTO(BaseModel):
    codigo_tipo_grupo: str


class ConsultaBensDisponiveisDTO(BaseModel):
    codigo_filial: str
    codigo_tipo_grupo: str
    codigo_tipo_venda: str


class ConsultaPrazosDisponiveisDTO(BaseModel):
    codigo_unidade: str
    codigo_tipo_grupo: str
    codigo_representante: str
    situacao_grupo: str = "A"  # A=Ativo, F=Fechado, X=Cancelado
    pessoa: str = "F"  # F=Física, J=Jurídica
    ordem_pesquisa: str = "G"  # G=Grupo, P=Prazo
    codigo_filial: str
    codigo_tipo_venda: Optional[str] = None
    codigo_bem: Optional[str] = None
    prazo: Optional[int] = None
    dia_vencimento: Optional[int] = None
    data_assembleia: Optional[str] = None
    codigo_grupo: Optional[str] = None
    sn_rateia: Optional[str] = "N"  # S=Sim, N=Não


class ConsultaRegraCobrancaDTO(BaseModel):
    codigo_plano: str
    codigo_tipo_venda: str
    codigo_bem: str
    codigo_tipo_grupo: str
    codigo_filial: str
    rateia: str
    numero_assembleia_emissao: str
    prazo: int
    sequencia_agrupamento: str


# DTOs de saída
class TipoGrupoOutDTO(BaseModel):
    codigo: str
    descricao: str


class FilialVendaOutDTO(BaseModel):
    codigo: str
    nome: str


class TipoVendaOutDTO(BaseModel):
    codigo: str
    descricao: str


class BemDisponivelOutDTO(BaseModel):
    codigo: str
    descricao: str
    valor: Decimal


class BemDisponivelPorGrupoOutDTO(BaseModel):
    codigo_grupo: str
    codigo_bem: str
    descricao: str
    valor: Decimal


class PrazoDisponivelOutDTO(BaseModel):
    codigo_grupo: str
    prazo_venda: Optional[int] = None
    prazo_grupo: Optional[int] = None
    dia_vencimento: Optional[int] = None
    valor_prestacao: Optional[Decimal] = None
    codigo_bem: str
    valor_bem: Decimal
    codigo_plano: str
    sequencia_agrupamento: str
    percentual_taxa_adm: Optional[Decimal] = None
    percentual_fundo_reserva: Optional[Decimal] = None
    percentual_mensal: Optional[Decimal] = None
    data_proxima_assembleia: Optional[str] = None
    cotas_vagas: Optional[int] = None
    data_vencimento_limite: Optional[str] = None


class FaixaParcelaOutDTO(BaseModel):
    faixa_inicial: int
    faixa_final: int
    percentual_fundo_comum: Decimal
    percentual_taxa_adm: Decimal
    percentual_fundo_reserva: Decimal
    percentual_seguros: Optional[Decimal] = None
    valor_parcela: Decimal


class RegraCobrancaOutDTO(BaseModel):
    codigo_plano: str
    prazo: int
    sequencia_agrupamento: str
    faixas_parcelas: List[FaixaParcelaOutDTO]


# DTOs de resposta da API
class CatalogoResponseDTO(BaseModel):
    sucesso: bool
    mensagem: str
    dados: Optional[dict] = None
    erro: Optional[str] = None
