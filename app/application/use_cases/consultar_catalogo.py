"""
Módulo contendo os casos de uso para consulta do catálogo de consórcios.
"""

from typing import List
from app.domain.repositories.catalogo_repo import CatalogoRepository
from app.domain.entities.catalogo import (
    TipoGrupo,
    FilialVenda,
    TipoVenda,
    BemDisponivel,
    BemDisponivelPorGrupo,
    PrazoDisponivel,
    RegraCobranca,
)
from app.application.dto.catalogo_dto import (
    ConsultaTiposVendasDTO,
    ConsultaBensDisponiveisDTO,
    ConsultaPrazosDisponiveisDTO,
    ConsultaRegraCobrancaDTO,
)


class ConsultarCatalogoUseCase:
    """
    Caso de uso responsável por consultar o catálogo de consórcios.
    """

    def __init__(self, repo: CatalogoRepository):
        self.repo = repo

    async def consultar_tipos_grupos(self) -> List[TipoGrupo]:
        """Consulta tipos de grupos (categorias)"""
        return await self.repo.consultar_tipos_grupos()

    async def consultar_filiais_vendas(self) -> List[FilialVenda]:
        """Consulta filiais de venda"""
        return await self.repo.consultar_filiais_vendas()

    async def consultar_tipos_vendas(
        self, dto: ConsultaTiposVendasDTO
    ) -> List[TipoVenda]:
        """Consulta tipos de venda por categoria"""
        return await self.repo.consultar_tipos_vendas(dto.codigo_tipo_grupo)

    async def consultar_bens_disponiveis(
        self, dto: ConsultaBensDisponiveisDTO
    ) -> List[BemDisponivel]:
        """Consulta bens disponíveis para consórcio"""
        return await self.repo.consultar_bens_disponiveis(
            dto.codigo_filial, dto.codigo_tipo_grupo, dto.codigo_tipo_venda
        )

    async def consultar_bens_disponiveis_por_grupo(
        self, dto: ConsultaBensDisponiveisDTO
    ) -> List[BemDisponivelPorGrupo]:
        """Consulta bens disponíveis amarrados a grupos"""
        return await self.repo.consultar_bens_disponiveis_por_grupo(
            dto.codigo_filial, dto.codigo_tipo_grupo, dto.codigo_tipo_venda
        )

    async def consultar_prazos_disponiveis(
        self, dto: ConsultaPrazosDisponiveisDTO
    ) -> List[PrazoDisponivel]:
        """Consulta prazos e opções comerciais disponíveis"""
        return await self.repo.consultar_prazos_disponiveis(
            codigo_unidade=dto.codigo_unidade,
            codigo_tipo_grupo=dto.codigo_tipo_grupo,
            codigo_representante=dto.codigo_representante,
            situacao_grupo=dto.situacao_grupo,
            pessoa=dto.pessoa,
            ordem_pesquisa=dto.ordem_pesquisa,
            codigo_filial=dto.codigo_filial,
            codigo_tipo_venda=dto.codigo_tipo_venda,
            codigo_bem=dto.codigo_bem,
            prazo=dto.prazo,
            dia_vencimento=dto.dia_vencimento,
            data_assembleia=dto.data_assembleia,
            codigo_grupo=dto.codigo_grupo,
            sn_rateia=dto.sn_rateia,
        )

    async def consultar_regra_cobranca(
        self, dto: ConsultaRegraCobrancaDTO
    ) -> RegraCobranca:
        """Consulta regras de cobrança e composição da parcela"""
        return await self.repo.consultar_regra_cobranca(
            codigo_plano=dto.codigo_plano,
            codigo_tipo_venda=dto.codigo_tipo_venda,
            codigo_bem=dto.codigo_bem,
            codigo_tipo_grupo=dto.codigo_tipo_grupo,
            codigo_filial=dto.codigo_filial,
            rateia=dto.rateia,
            numero_assembleia_emissao=dto.numero_assembleia_emissao,
            prazo=dto.prazo,
            sequencia_agrupamento=dto.sequencia_agrupamento,
        )
