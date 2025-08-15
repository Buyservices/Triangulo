# app/infrastructure/mappers/mappers_new.py

from typing import Dict, Any


def map_cliente_to_form(cliente: Dict[str, Any]) -> Dict[str, str]:
    """
    Converte o payload JSON vindo do cliente para o formato form-data
    aceito pelo endpoint da Newcon (prcManutencaoCliente_new).
    Envia apenas campos essenciais para evitar erros de conversão.
    """

    form = {}

    # Campos obrigatórios (sempre enviados)
    form["Cliente_Novo"] = cliente.get("Cliente_Novo", "S")
    form["Valida_Dados_Conjuge"] = cliente.get("Valida_Dados_Conjuge", "N")
    form["Politicamente_Exposto"] = cliente.get("Politicamente_Exposto", "N")
    form["Cgc_Cpf_Cliente"] = cliente.get("Cgc_Cpf_Cliente", "")
    form["Nome"] = cliente.get("Nome", "")
    form["Pessoa"] = cliente.get("Pessoa", "")
    form["Documento"] = cliente.get("Documento", "")
    form["Codigo_Tipo_Doc_Ident"] = str(cliente.get("Codigo_Tipo_Doc_Ident", ""))
    form["UF_Doc_Cliente"] = cliente.get("UF_Doc_Cliente", "")
    form["Data_Exp_Doc"] = cliente.get("Data_Exp_Doc") or "01/01/2000"

    # Endereço principal (obrigatório)
    endereco = None
    if "ws_stcEndereco" in cliente and cliente["ws_stcEndereco"]:
        endereco = cliente["ws_stcEndereco"][0]

    if endereco:
        form["Insere_Endereco_Residencial"] = "S"
        form["Endereco"] = endereco.get("Endereco", "")
        form["Bairro"] = endereco.get("Bairro", "")
        form["Cidade"] = endereco.get("Cidade", "")
        form["CEP"] = endereco.get("CEP", "")
        form["Estado"] = endereco.get("Estado", "")
    else:
        form["Insere_Endereco_Residencial"] = "N"

    # Campos obrigatórios adicionais identificados pela API
    form["Orgao_Emissor"] = cliente.get("Orgao_Emissor", "SSP")
    form["Naturalidade"] = cliente.get("Naturalidade", "São Paulo")
    form["Nacionalidade"] = cliente.get("Nacionalidade", "Brasileira")
    form["Renda"] = cliente.get("Renda", "0")
    form["Estado_Civil"] = cliente.get("Estado_Civil", "S")
    form["Regime_Casamento"] = cliente.get("Regime_Casamento", "C")
    form["Sexo"] = cliente.get("Sexo", "F")
    form["Nivel_Ensino"] = cliente.get("Nivel_Ensino", "1")
    form["Codigo_Profissao"] = cliente.get("Codigo_Profissao", "1")
    form["Codigo_Atividade_Juridica"] = cliente.get("Codigo_Atividade_Juridica", "1")
    form["Codigo_Constituicao_Juridica"] = cliente.get("Codigo_Constituicao_Juridica", "1")
    form["Complemento"] = cliente.get("Complemento", "")
    form["DDD"] = cliente.get("DDD", "11")
    form["Fone_Fax"] = cliente.get("Fone_Fax", "")
    form["Insere_Endereco_Comercial"] = "N"
    form["Insere_Endereco_Outro"] = "N"

    # Campos obrigatórios adicionais identificados pela API
    form["Data_Nascimento"] = cliente.get("Data_Nascimento") or "01/01/1990"

    # Campos obrigatórios da documentação oficial (todos os demais)
    form["E_Mail"] = cliente.get("E_Mail", "")
    form["Celular"] = cliente.get("Celular", "")
    
    # Campos de endereço comercial (obrigatórios)
    form["Endereco_Comercial"] = ""
    form["Complemento_Comercial"] = ""
    form["Bairro_Comercial"] = ""
    form["Cidade_Comercial"] = ""
    form["CEP_Comercial"] = ""
    form["Estado_Comercial"] = ""
    form["DDD_Comercial"] = "11"
    form["Fone_Fax_Comercial"] = ""
    
    # Campos de endereço outro (obrigatórios)
    form["Endereco_Outro"] = ""
    form["Complemento_Outro"] = ""
    form["Bairro_Outro"] = ""
    form["Cidade_Outro"] = ""
    form["CEP_Outro"] = ""
    form["Estado_Outro"] = ""
    form["DDD_Outro"] = "11"
    form["Fone_Fax_Outro"] = ""
    
    # Campos do cônjuge (obrigatórios)
    form["Cpf_Conjuge"] = ""
    form["Nome_Conjuge"] = ""
    form["Data_Nascimento_Conjuge"] = "01/01/1990"
    form["Documento_Conjuge"] = ""
    form["Codigo_Tipo_Doc_Ident_Conj"] = "1"
    form["Orgao_Emissor_Conjuge"] = "SSP"
    form["Data_Exp_Doc_Conjuge"] = "01/01/2000"
    form["UF_Doc_Conjuge"] = "SP"
    form["Naturalidade_Conjuge"] = "São Paulo"
    form["Nacionalidade_Conjuge"] = "Brasileira"
    form["Codigo_Profissao_Conjuge"] = "1"

    return form
