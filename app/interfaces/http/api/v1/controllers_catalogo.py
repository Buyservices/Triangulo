"""
Controllers para operações do catálogo de consórcios.
"""

from app.application.use_cases.consultar_catalogo import ConsultarCatalogoUseCase
from app.application.dto.catalogo_dto import (
    ConsultaTiposVendasDTO,
    ConsultaBensDisponiveisDTO,
    ConsultaPrazosDisponiveisDTO,
    ConsultaRegraCobrancaDTO,
)
from app.interfaces.http.api.v1.schemas_catalogo import (
    ListaTiposGruposSchema,
    ListaFiliaisSchema,
    ListaTiposVendasSchema,
    ListaBensDisponiveisSchema,
    ListaPrazosDisponiveisSchema,
    RegraCobrancaSchema,
)


async def get_categorias(uc: ConsultarCatalogoUseCase) -> ListaTiposGruposSchema:
    """
    Consulta todas as categorias de consórcio disponíveis.
    
    Retorna uma lista completa de categorias como Imóveis, Veículos, Motocicletas, etc.
    Esta consulta não requer parâmetros e retorna dados estáticos da base Newcon.
    
    **Integração**: Chama o método `cnsTiposGrupos` do WebService SOAP da Newcon.
    **Cache**: Recomendado para dados que mudam raramente.
    """
    try:
        tipos_grupos = await uc.consultar_tipos_grupos()

        # Converte para schemas de saída
        categorias = []
        for tipo in tipos_grupos:
            categorias.append(
                {"codigo": tipo.Codigo_Tipo_Grupo, "descricao": tipo.Descricao}
            )

        return ListaTiposGruposSchema(
            sucesso=True,
            mensagem=f"Encontradas {len(categorias)} categorias",
            categorias=categorias,
        )

    except Exception as e:
        return ListaTiposGruposSchema(
            sucesso=False,
            mensagem="Erro ao consultar categorias",
            categorias=[],
            erro=str(e),
        )


async def get_filiais(uc: ConsultarCatalogoUseCase) -> ListaFiliaisSchema:
    """
    Consulta todas as filiais de venda cadastradas no sistema.
    
    Retorna a lista de filiais onde é possível realizar vendas de consórcio.
    Esta consulta não requer parâmetros e retorna dados estáticos da base Newcon.
    
    **Integração**: Chama o método `cnsFiliaisVendas` do WebService SOAP da Newcon.
    **Cache**: Recomendado para dados que mudam raramente.
    """
    try:
        filiais = await uc.consultar_filiais_vendas()

        # Converte para schemas de saída
        filiais_out = []
        for filial in filiais:
            filiais_out.append(
                {"codigo": filial.Codigo_Filial_Venda, "nome": filial.Nome_Filial_Venda}
            )

        return ListaFiliaisSchema(
            sucesso=True,
            mensagem=f"Encontradas {len(filiais_out)} filiais",
            filiais=filiais_out,
        )

    except Exception as e:
        return ListaFiliaisSchema(
            sucesso=False, mensagem="Erro ao consultar filiais", filiais=[], erro=str(e)
        )


async def get_tipos_venda(
    tipo_grupo: str, uc: ConsultarCatalogoUseCase
) -> ListaTiposVendasSchema:
    """
    Consulta os tipos de venda disponíveis para uma categoria específica.
    
    Retorna os tipos de comercialização (ex: Venda Direta, Consórcio) disponíveis
    para uma categoria como Imóveis, Veículos, etc.
    
    **Parâmetros**:
    - `tipo_grupo`: Código da categoria (ex: IM=Imóveis, AI=Automóveis Importados)
    
    **Integração**: Chama o método `cnsTiposVendas` do WebService SOAP da Newcon.
    **Nota**: Nem todas as categorias possuem tipos de venda cadastrados.
    """
    try:
        dto = ConsultaTiposVendasDTO(codigo_tipo_grupo=tipo_grupo)
        tipos_venda = await uc.consultar_tipos_vendas(dto)

        # Converte para schemas de saída
        tipos_out = []
        for tipo in tipos_venda:
            tipos_out.append(
                {"codigo": tipo.Codigo_Tipo_Venda, "descricao": tipo.Descricao}
            )

        return ListaTiposVendasSchema(
            sucesso=True,
            mensagem=f"Encontrados {len(tipos_out)} tipos de venda para categoria {tipo_grupo}",
            tipos_venda=tipos_out,
        )

    except Exception as e:
        return ListaTiposVendasSchema(
            sucesso=False,
            mensagem="Erro ao consultar tipos de venda",
            tipos_venda=[],
            erro=str(e),
        )


async def get_bens_disponiveis(
    filial: str, tipo_grupo: str, tipo_venda: str, uc: ConsultarCatalogoUseCase
) -> ListaBensDisponiveisSchema:
    """
    Consulta os bens (cartas de crédito) disponíveis para uma combinação específica.
    
    Retorna a lista de bens disponíveis com seus valores e descrições para
    uma filial, categoria e tipo de venda específicos.
    
    **Parâmetros**:
    - `filial`: Código da filial (ex: 1=TRIANGULO ADM.)
    - `tipo_grupo`: Código da categoria (ex: IM=Imóveis, AI=Automóveis)
    - `tipo_venda`: Código do tipo de venda (ex: 10, 20)
    
    **Integração**: Chama o método `cnsBensDisponiveis` do WebService SOAP da Newcon.
    **Resultado**: Lista de cartas de crédito disponíveis com valores.
    """
    try:
        dto = ConsultaBensDisponiveisDTO(
            codigo_filial=filial,
            codigo_tipo_grupo=tipo_grupo,
            codigo_tipo_venda=tipo_venda,
        )
        bens = await uc.consultar_bens_disponiveis(dto)

        # Converte para schemas de saída
        bens_out = []
        for bem in bens:
            bens_out.append(
                {
                    "codigo": bem.Codigo_Bem,
                    "descricao": bem.Descricao,
                    "valor": bem.Valor_Bem,
                }
            )

        return ListaBensDisponiveisSchema(
            sucesso=True,
            mensagem=f"Encontrados {len(bens_out)} bens disponíveis",
            bens=bens_out,
        )

    except Exception as e:
        return ListaBensDisponiveisSchema(
            sucesso=False,
            mensagem="Erro ao consultar bens disponíveis",
            bens=[],
            erro=str(e),
        )


async def get_prazos_disponiveis(
    unidade: str,
    tipo_grupo: str,
    representante: str,
    filial: str,
    situacao_grupo: str = "A",
    pessoa: str = "F",
    ordem_pesquisa: str = "G",
    tipo_venda: str = None,
    bem: str = None,
    prazo: int = None,
    dia_vencimento: int = None,
    data_assembleia: str = None,
    codigo_grupo: str = None,
    rateia: str = "N",
    uc: ConsultarCatalogoUseCase = None,
) -> ListaPrazosDisponiveisSchema:
    """
    Consulta as opções comerciais disponíveis (prazos, prestações, planos).
    
    Retorna as opções de financiamento disponíveis incluindo prazos, valores de
    prestação, planos e informações sobre assembleias e cotas vagas.
    
    **Parâmetros Obrigatórios**:
    - `unidade`: Código da unidade administrativa
    - `tipo_grupo`: Código da categoria (ex: IM=Imóveis)
    - `representante`: Código do representante comercial
    - `filial`: Código da filial (ex: 1=TRIANGULO ADM.)
    
    **Parâmetros Opcionais**:
    - `situacao_grupo`: A=Ativo, F=Fechado, X=Cancelado
    - `pessoa`: F=Física, J=Jurídica
    - `rateia`: S=Sim, N=Não
    
    **Integração**: Chama o método `cnsPrazosDisponiveis` do WebService SOAP da Newcon.
    **Resultado**: Opções comerciais completas para montar a vitrine.
    """
    try:
        dto = ConsultaPrazosDisponiveisDTO(
            codigo_unidade=unidade,
            codigo_tipo_grupo=tipo_grupo,
            codigo_representante=representante,
            situacao_grupo=situacao_grupo,
            pessoa=pessoa,
            ordem_pesquisa=ordem_pesquisa,
            codigo_filial=filial,
            codigo_tipo_venda=tipo_venda,
            codigo_bem=bem,
            prazo=prazo,
            dia_vencimento=dia_vencimento,
            data_assembleia=data_assembleia,
            codigo_grupo=codigo_grupo,
            sn_rateia=rateia,
        )
        prazos = await uc.consultar_prazos_disponiveis(dto)

        # Converte para schemas de saída
        prazos_out = []
        for prazo in prazos:
            prazos_out.append(
                {
                    "codigo_grupo": prazo.Codigo_Grupo,
                    "prazo_venda": prazo.Prazo_Venda,
                    "prazo_grupo": prazo.Prazo_Grupo,
                    "dia_vencimento": prazo.Dia_Vencimento,
                    "valor_prestacao": prazo.Valor_Prestacao,
                    "codigo_bem": prazo.Codigo_Bem,
                    "valor_bem": prazo.Valor_Bem,
                    "codigo_plano": prazo.Codigo_Plano,
                    "sequencia_agrupamento": prazo.Sequencia_Agrupamento,
                    "percentual_taxa_adm": prazo.Percentual_Taxa_Adm,
                    "percentual_fundo_reserva": prazo.Percentual_Fundo_Reserva,
                    "percentual_mensal": prazo.Percentual_Mensal,
                    "data_proxima_assembleia": prazo.Data_Proxima_Assembleia,
                    "cotas_vagas": prazo.Qtde_Cotas_Vagas,
                    "data_vencimento_limite": prazo.Data_Vencimento_Limite,
                }
            )

        return ListaPrazosDisponiveisSchema(
            sucesso=True,
            mensagem=f"Encontrados {len(prazos_out)} prazos disponíveis",
            prazos=prazos_out,
        )

    except Exception as e:
        return ListaPrazosDisponiveisSchema(
            sucesso=False,
            mensagem="Erro ao consultar prazos disponíveis",
            prazos=[],
            erro=str(e),
        )


async def get_regra_cobranca(
    plano: str,
    tipo_venda: str,
    bem: str,
    tipo_grupo: str,
    filial: str,
    rateia: str,
    numero_assembleia_emissao: str,
    prazo: int,
    sequencia_agrupamento: str,
    uc: ConsultarCatalogoUseCase,
) -> RegraCobrancaSchema:
    """
    Consulta a composição detalhada das parcelas de um plano específico.
    
    Retorna o breakdown financeiro completo incluindo percentuais de taxa
    administrativa, fundo de reserva, seguros e valor calculado por faixa.
    
    **Parâmetros Obrigatórios**:
    - `plano`: Código do plano de consórcio
    - `tipo_venda`: Código do tipo de venda
    - `bem`: Código do bem específico
    - `tipo_grupo`: Código da categoria
    - `filial`: Código da filial
    - `rateia`: S=Sim, N=Não
    - `numero_assembleia_emissao`: Número da assembleia
    - `prazo`: Prazo em meses
    - `sequencia_agrupamento`: Sequência de agrupamento
    
    **Integração**: Chama o método `cnsRegraCobranca` do WebService SOAP da Newcon.
    **Resultado**: Composição financeira detalhada para simulação precisa.
    """
    try:
        dto = ConsultaRegraCobrancaDTO(
            codigo_plano=plano,
            codigo_tipo_venda=tipo_venda,
            codigo_bem=bem,
            codigo_tipo_grupo=tipo_grupo,
            codigo_filial=filial,
            rateia=rateia,
            numero_assembleia_emissao=numero_assembleia_emissao,
            prazo=prazo,
            sequencia_agrupamento=sequencia_agrupamento,
        )
        regra = await uc.consultar_regra_cobranca(dto)

        # Converte para schema de saída
        faixas_out = []
        for faixa in regra.Faixas_Parcelas:
            faixas_out.append(
                {
                    "faixa_inicial": faixa.Faixa_Inicial,
                    "faixa_final": faixa.Faixa_Final,
                    "percentual_fundo_comum": faixa.Percentual_Fundo_Comum,
                    "percentual_taxa_adm": faixa.Percentual_Taxa_Adm,
                    "percentual_fundo_reserva": faixa.Percentual_Fundo_Reserva,
                    "percentual_seguros": faixa.Percentual_Seguros,
                    "valor_parcela": faixa.Valor_Parcela,
                }
            )

        return RegraCobrancaSchema(
            codigo_plano=regra.Codigo_Plano,
            prazo=regra.Prazo,
            sequencia_agrupamento=regra.Sequencia_Agrupamento,
            faixas_parcelas=faixas_out,
        )

    except Exception as e:
        # Para erro, retorna schema vazio com erro
        raise Exception(f"Erro ao consultar regra de cobrança: {str(e)}")
