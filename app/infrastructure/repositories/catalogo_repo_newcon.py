"""
Repositório de catálogo que integra com WebServices SOAP da Newcon.
"""

from typing import List, Optional
from decimal import Decimal
from app.domain.repositories.catalogo_repo import CatalogoRepository
from app.domain.entities.catalogo import (
    TipoGrupo,
    FilialVenda,
    TipoVenda,
    BemDisponivel,
    BemDisponivelPorGrupo,
    PrazoDisponivel,
    RegraCobranca,
    FaixaParcela,
)
from app.infrastructure.http.newcon_soap_client import NewconSoapClient
from app.infrastructure.config.settings import Settings


class CatalogoRepositoryNewcon(CatalogoRepository):
    """
    Implementação do repositório de catálogo que integra com Newcon.
    """

    def __init__(self, soap_client: Optional[NewconSoapClient] = None):
        settings = Settings()
        self.soap_client = soap_client or NewconSoapClient(
            base_url=settings.soap_base_url, timeout=settings.soap_timeout
        )

    async def consultar_tipos_grupos(self) -> List[TipoGrupo]:
        """Consulta tipos de grupos (categorias) via cnsTiposGrupos"""
        try:
            # Chama método SOAP sem parâmetros
            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsTiposGrupos", {}
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            # Verifica se há erro na resposta
            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            # Parse da resposta SOAP
            parsed_response = self.soap_client.parse_soap_response(response_text)

            # Converte para entidades de domínio
            tipos_grupos = []

            # Procura por dados na resposta
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    tipos_grupos.append(
                        TipoGrupo(
                            Codigo_Tipo_Grupo=row.get("CODIGO_TIPO_GRUPO", ""),
                            Descricao=row.get("DESCRICAO", ""),
                        )
                    )
            else:
                # Fallback para estrutura simples
                for key, value in parsed_response.items():
                    if "Codigo_Tipo_Grupo" in key or "Descricao" in key:
                        # Lógica para extrair dados da estrutura simples
                        pass

            return tipos_grupos

        except Exception as e:
            # Log do erro para debug
            print(f"Erro ao consultar tipos de grupos: {str(e)}")
            raise

    async def consultar_filiais_vendas(self) -> List[FilialVenda]:
        """Consulta filiais de venda via cnsFiliaisVendas"""
        try:
            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsFiliaisVendas", {}
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            filiais = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    filiais.append(
                        FilialVenda(
                            Codigo_Filial_Venda=row.get("CODIGO_FILIAL_VENDA", ""),
                            Nome_Filial_Venda=row.get("NOME_FILIAL_VENDA", ""),
                        )
                    )

            return filiais

        except Exception as e:
            print(f"Erro ao consultar filiais de venda: {str(e)}")
            raise

    async def consultar_tipos_vendas(self, codigo_tipo_grupo: str) -> List[TipoVenda]:
        """Consulta tipos de venda por categoria via cnsTiposVendas"""
        try:
            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsTiposVendas", {"Codigo_Tipo_Grupo": codigo_tipo_grupo}
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            tipos_venda = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    tipos_venda.append(
                        TipoVenda(
                            Codigo_Tipo_Venda=row.get("CODIGO_TIPO_VENDA", ""),
                            Descricao=row.get("DESCRICAO", ""),
                        )
                    )

            return tipos_venda

        except Exception as e:
            print(f"Erro ao consultar tipos de venda: {str(e)}")
            raise

    async def consultar_bens_disponiveis(
        self, codigo_filial: str, codigo_tipo_grupo: str, codigo_tipo_venda: str
    ) -> List[BemDisponivel]:
        """Consulta bens disponíveis via cnsBensDisponiveis"""
        try:
            params = {
                "Codigo_Filial": codigo_filial,
                "Codigo_Tipo_Grupo": codigo_tipo_grupo,
                "Codigo_Tipo_Venda": codigo_tipo_venda,
            }

            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsBensDisponiveis", params
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            bens = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    bens.append(
                        BemDisponivel(
                            Codigo_Bem=row.get("CODIGO_BEM", ""),
                            Descricao=row.get("DESCRICAO", ""),
                            Valor_Bem=Decimal(row.get("VALOR_BEM", "0")),
                        )
                    )

            return bens

        except Exception as e:
            print(f"Erro ao consultar bens disponíveis: {str(e)}")
            raise

    async def consultar_bens_disponiveis_por_grupo(
        self, codigo_filial: str, codigo_tipo_grupo: str, codigo_tipo_venda: str
    ) -> List[BemDisponivelPorGrupo]:
        """Consulta bens disponíveis amarrados a grupos via cnsBensDisponiveisPorGrupo"""
        try:
            params = {
                "Codigo_Filial": codigo_filial,
                "Codigo_Tipo_Grupo": codigo_tipo_grupo,
                "Codigo_Tipo_Venda": codigo_tipo_venda,
            }

            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsBensDisponiveisPorGrupo", params
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            bens = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    bens.append(
                        BemDisponivelPorGrupo(
                            Codigo_Grupo=row.get("CODIGO_GRUPO", ""),
                            Codigo_Bem=row.get("CODIGO_BEM", ""),
                            Descricao=row.get("DESCRICAO", ""),
                            Valor_Bem=Decimal(row.get("VALOR_BEM", "0")),
                        )
                    )

            return bens

        except Exception as e:
            print(f"Erro ao consultar bens por grupo: {str(e)}")
            raise

    async def consultar_prazos_disponiveis(
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
        """Consulta prazos disponíveis via cnsPrazosDisponiveis"""
        try:
            params = {
                "Codigo_Unidade": codigo_unidade,
                "Codigo_Tipo_Grupo": codigo_tipo_grupo,
                "Codigo_Representante": codigo_representante,
                "Situacao_Grupo": situacao_grupo,
                "Pessoa": pessoa,
                "Ordem_Pesquisa": ordem_pesquisa,
                "Codigo_Filial": codigo_filial,
            }

            # Adiciona parâmetros opcionais
            if codigo_tipo_venda:
                params["Codigo_Tipo_Venda"] = codigo_tipo_venda
            if codigo_bem:
                params["Codigo_Bem"] = codigo_bem
            if prazo:
                params["Prazo"] = prazo
            if dia_vencimento:
                params["Dia_Vencimento"] = dia_vencimento
            if data_assembleia:
                params["Data_Assembleia"] = data_assembleia
            if codigo_grupo:
                params["Codigo_Grupo"] = codigo_grupo
            if sn_rateia:
                params["SN_Rateia"] = sn_rateia

            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsPrazosDisponiveis", params
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            prazos = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    prazos.append(
                        PrazoDisponivel(
                            Codigo_Grupo=row.get("CODIGO_GRUPO", ""),
                            Prazo_Venda=(
                                int(row.get("PRAZO_VENDA", "0"))
                                if row.get("PRAZO_VENDA")
                                else None
                            ),
                            Prazo_Grupo=(
                                int(row.get("PRAZO_GRUPO", "0"))
                                if row.get("PRAZO_GRUPO")
                                else None
                            ),
                            Dia_Vencimento=(
                                int(row.get("DIA_VENCIMENTO", "0"))
                                if row.get("DIA_VENCIMENTO")
                                else None
                            ),
                            Valor_Prestacao=(
                                Decimal(row.get("VALOR_PRESTACAO", "0"))
                                if row.get("VALOR_PRESTACAO")
                                else None
                            ),
                            Codigo_Bem=row.get("CODIGO_BEM", ""),
                            Valor_Bem=Decimal(row.get("VALOR_BEM", "0")),
                            Codigo_Plano=row.get("CODIGO_PLANO", ""),
                            Sequencia_Agrupamento=row.get("SEQUENCIA_AGRUPAMENTO", ""),
                            Percentual_Taxa_Adm=(
                                Decimal(row.get("PERCENTUAL_TAXA_ADM", "0"))
                                if row.get("PERCENTUAL_TAXA_ADM")
                                else None
                            ),
                            Percentual_Fundo_Reserva=(
                                Decimal(row.get("PERCENTUAL_FUNDO_RESERVA", "0"))
                                if row.get("PERCENTUAL_FUNDO_RESERVA")
                                else None
                            ),
                            Percentual_Mensal=(
                                Decimal(row.get("PERCENTUAL_MENSAL", "0"))
                                if row.get("PERCENTUAL_MENSAL")
                                else None
                            ),
                            Data_Proxima_Assembleia=row.get("DATA_PROXIMA_ASSEMBLEIA"),
                            Qtde_Cotas_Vagas=(
                                int(row.get("QTDE_COTAS_VAGAS", "0"))
                                if row.get("QTDE_COTAS_VAGAS")
                                else None
                            ),
                            Data_Vencimento_Limite=row.get("DATA_VENCIMENTO_LIMITE"),
                        )
                    )

            return prazos

        except Exception as e:
            print(f"Erro ao consultar prazos disponíveis: {str(e)}")
            raise

    async def consultar_regra_cobranca(
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
        """Consulta regras de cobrança via cnsRegraCobranca"""
        try:
            params = {
                "Codigo_Plano": codigo_plano,
                "Codigo_Tipo_Venda": codigo_tipo_venda,
                "Codigo_Bem": codigo_bem,
                "Codigo_Tipo_Grupo": codigo_tipo_grupo,
                "Codigo_Filial": codigo_filial,
                "Rateia": rateia,
                "Numero_Assembleia_Emissao": numero_assembleia_emissao,
                "Prazo": prazo,
                "Sequencia_Agrupamento": sequencia_agrupamento,
            }

            status_code, response_text = await self.soap_client.call_soap_method(
                "cnsRegraCobranca", params
            )

            if status_code != 200:
                raise Exception(f"Erro HTTP {status_code}: {response_text}")

            error_msg = self.soap_client.check_error_response(response_text)
            if error_msg:
                raise Exception(f"Erro Newcon: {error_msg}")

            parsed_response = self.soap_client.parse_soap_response(response_text)

            # Constrói entidade RegraCobranca
            faixas_parcelas = []
            if "Table" in parsed_response:
                for row in parsed_response["Table"]:
                    faixas_parcelas.append(
                        FaixaParcela(
                            Faixa_Inicial=int(row.get("FAIXA_INICIAL", "0")),
                            Faixa_Final=int(row.get("FAIXA_FINAL", "0")),
                            Percentual_Fundo_Comum=Decimal(
                                row.get("PERCENTUAL_FUNDO_COMUM", "0")
                            ),
                            Percentual_Taxa_Adm=Decimal(
                                row.get("PERCENTUAL_TAXA_ADM", "0")
                            ),
                            Percentual_Fundo_Reserva=Decimal(
                                row.get("PERCENTUAL_FUNDO_RESERVA", "0")
                            ),
                            Percentual_Seguros=(
                                Decimal(row.get("PERCENTUAL_SEGUROS", "0"))
                                if row.get("PERCENTUAL_SEGUROS")
                                else None
                            ),
                            Valor_Parcela=Decimal(row.get("VALOR_PARCELA", "0")),
                        )
                    )

            return RegraCobranca(
                Codigo_Plano=codigo_plano,
                Prazo=prazo,
                Sequencia_Agrupamento=sequencia_agrupamento,
                Faixas_Parcelas=faixas_parcelas,
            )

        except Exception as e:
            print(f"Erro ao consultar regra de cobrança: {str(e)}")
            raise
