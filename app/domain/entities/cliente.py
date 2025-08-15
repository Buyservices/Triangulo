from pydantic import BaseModel
from typing import List, Optional


class Endereco(BaseModel):
    Tipo_Endereco: str
    Endereco: str
    Bairro: str
    Cidade: str
    CEP: str
    Estado: str


class Cliente(BaseModel):
    Cliente_Novo: str
    Valida_Dados_Conjuge: str
    Politicamente_Exposto: str
    Cgc_Cpf_Cliente: str
    Nome: str
    Pessoa: str
    Documento: str
    Codigo_Tipo_Doc_Ident: int
    UF_Doc_Cliente: str
    Data_Exp_Doc: Optional[str] = None
    ws_stcEndereco: List[Endereco]
