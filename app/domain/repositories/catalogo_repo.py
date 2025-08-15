from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.catalogo import (
    TipoGrupo,
    FilialVenda,
    TipoVenda,
    BemDisponivel,
    BemDisponivelPorGrupo,
    PrazoDisponivel,
    RegraCobranca,
)


class CatalogoRepository(ABC):
    """Contrato para repositório de catálogo de consórcios"""

    @abstractmethod
    def consultar_tipos_grupos(self) -> List[TipoGrupo]:
        """Consulta tipos de grupos (categorias)"""
        pass

    @abstractmethod
    def consultar_filiais_vendas(self) -> List[FilialVenda]:
        """Consulta filiais de venda"""
        pass

    @abstractmethod
    def consultar_tipos_vendas(self, codigo_tipo_grupo: str) -> List[TipoVenda]:
        """Consulta tipos de venda por categoria"""
        pass

    @abstractmethod
    def consultar_bens_disponiveis(
        self, codigo_filial: str, codigo_tipo_grupo: str, codigo_tipo_venda: str
    ) -> List[BemDisponivel]:
        """Consulta bens disponíveis para consórcio"""
        pass

    @abstractmethod
    def consultar_bens_disponiveis_por_grupo(
        self, codigo_filial: str, codigo_tipo_grupo: str, codigo_tipo_venda: str
    ) -> List[BemDisponivelPorGrupo]:
        """Consulta bens disponíveis amarrados a grupos"""
        pass

    @abstractmethod
    def consultar_prazos_disponiveis(
        self,
        codigo_unidade: str,
        codigo_tipo_grupo: str,
        codigo_representante: str,
        situacao_grupo: str,
        pessoa: str,
        ordem_pesquisa: str,
        codigo_filial: str,
        codigo_tipo_venda: Optional[str] = None,
        codigo_bem: Optional[str] = None,
        prazo: Optional[int] = None,
        dia_vencimento: Optional[int] = None,
        data_assembleia: Optional[str] = None,
        codigo_grupo: Optional[str] = None,
        sn_rateia: Optional[str] = None,
    ) -> List[PrazoDisponivel]:
        """Consulta prazos e opções comerciais disponíveis"""
        pass

    @abstractmethod
    def consultar_regra_cobranca(
        self,
        codigo_plano: str,
        codigo_tipo_venda: str,
        codigo_bem: str,
        codigo_tipo_grupo: str,
        codigo_filial: str,
        rateia: str,
        numero_assembleia_emissao: str,
        prazo: int,
        sequencia_agrupamento: str,
    ) -> RegraCobranca:
        """Consulta regras de cobrança e composição da parcela"""
        pass
