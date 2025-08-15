from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class TipoGrupo(BaseModel):
    """Tipo de grupo (categoria: imóveis, veículos, etc.)"""
    Codigo_Tipo_Grupo: str
    Descricao: str


class FilialVenda(BaseModel):
    """Filial de venda"""
    Codigo_Filial_Venda: str
    Nome_Filial_Venda: str


class TipoVenda(BaseModel):
    """Tipo de venda por categoria"""
    Codigo_Tipo_Venda: str
    Descricao: str


class BemDisponivel(BaseModel):
    """Bem/carta disponível para consórcio"""
    Codigo_Bem: str
    Descricao: str
    Valor_Bem: Decimal


class BemDisponivelPorGrupo(BaseModel):
    """Bem disponível amarrado a um grupo específico"""
    Codigo_Grupo: str
    Codigo_Bem: str
    Descricao: str
    Valor_Bem: Decimal


class PrazoDisponivel(BaseModel):
    """Prazo/plano disponível para consórcio"""
    Codigo_Grupo: str
    Prazo_Venda: Optional[int] = None
    Prazo_Grupo: Optional[int] = None
    Dia_Vencimento: Optional[int] = None
    Valor_Prestacao: Optional[Decimal] = None
    Codigo_Bem: str
    Valor_Bem: Decimal
    Codigo_Plano: str
    Sequencia_Agrupamento: str
    Percentual_Taxa_Adm: Optional[Decimal] = None
    Percentual_Fundo_Reserva: Optional[Decimal] = None
    Percentual_Mensal: Optional[Decimal] = None
    Data_Proxima_Assembleia: Optional[str] = None
    Qtde_Cotas_Vagas: Optional[int] = None
    Data_Vencimento_Limite: Optional[str] = None


class RegraCobranca(BaseModel):
    """Composição da parcela com breakdown financeiro"""
    Codigo_Plano: str
    Prazo: int
    Sequencia_Agrupamento: str
    Faixas_Parcelas: List['FaixaParcela']


class FaixaParcela(BaseModel):
    """Faixa de parcelas com percentuais"""
    Faixa_Inicial: int
    Faixa_Final: int
    Percentual_Fundo_Comum: Decimal
    Percentual_Taxa_Adm: Decimal
    Percentual_Fundo_Reserva: Decimal
    Percentual_Seguros: Optional[Decimal] = None
    Valor_Parcela: Decimal


# Forward references
RegraCobranca.model_rebuild()
