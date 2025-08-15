from typing import Optional, List
from pydantic import BaseModel, EmailStr

class EnderecoDTO(BaseModel):
    Tipo_Endereco: str
    Endereco: str
    Complemento: Optional[str] = None
    Bairro: str
    Cidade: str
    CEP: str
    Estado: str
    DDD: Optional[str] = None
    Fone_Fax: Optional[str] = None

class ClienteInDTO(BaseModel):
    Cliente_Novo: str
    Valida_Dados_Conjuge: str = "N"
    Politicamente_Exposto: str = "N"
    Cgc_Cpf_Cliente: str
    Nome: str
    Pessoa: str
    Documento: str
    Codigo_Tipo_Doc_Ident: int
    Orgao_Emissor: Optional[str] = None
    Data_Exp_Doc: Optional[str] = None
    UF_Doc_Cliente: Optional[str] = None
    Naturalidade: Optional[str] = None
    Nacionalidade: Optional[str] = None
    Renda: Optional[float] = None
    Data_Nascimento: Optional[str] = None
    Estado_Civil: Optional[str] = None
    Regime_Casamento: Optional[str] = None
    Sexo: Optional[str] = None
    Nivel_Ensino: Optional[int] = None
    Codigo_Profissao: Optional[int] = None
    Codigo_Atividade_Juridica: Optional[int] = None
    Codigo_Constituicao_Juridica: Optional[int] = None
    E_Mail: Optional[EmailStr] = None
    Celular: Optional[str] = None
    Outro_Telefone: Optional[str] = None
    ws_stcEndereco: List[EnderecoDTO] = []

    # Cônjuge
    Cpf_Conjuge: Optional[str] = None
    Nome_Conjuge: Optional[str] = None
    Data_Nascimento_Conjuge: Optional[str] = None
    Documento_Conjuge: Optional[str] = None
    Codigo_Tipo_Doc_Ident_Conj: Optional[int] = None
    Orgao_Emissor_Conjuge: Optional[str] = None
    Data_Exp_Doc_Conjuge: Optional[str] = None
    UF_Doc_Conjuge: Optional[str] = None
    Naturalidade_Conjuge: Optional[str] = None
    Nacionalidade_Conjuge: Optional[str] = None
    Codigo_Profissao_Conjuge: Optional[int] = None

class ClienteOutDTO(BaseModel):
    sucesso: bool
    mensagem: str
    bruto_xml: str
