#!/usr/bin/env python3
"""
Cliente SOAP real para WebServices da Newcon
Envia requisições POST com envelope XML completo
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
import json

class NewconSoapClient:
    """Cliente SOAP para WebServices da Newcon"""
    
    def __init__(self, base_url: str = "https://webatendimento.consorciotriangulo.com.br/wsregvenda/wsRegVenda.asmx"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'http://www.cnpm.com.br/'
        }
    
    def _create_soap_envelope(self, method: str, params: Dict[str, str] = None) -> str:
        """Cria envelope SOAP com parâmetros"""
        
        # Parâmetros XML
        params_xml = ""
        if params:
            for key, value in params.items():
                params_xml += f"      <{key}>{value}</{key}>\n"
        
        # Envelope SOAP completo
        soap_envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <{method} xmlns="http://www.cnpm.com.br/">
{params_xml}    </{method}>
  </soap:Body>
</soap:Envelope>"""
        
        return soap_envelope
    
    def call_soap_method(self, method: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Chama método SOAP da Newcon"""
        
        try:
            # Cria envelope SOAP
            soap_body = self._create_soap_envelope(method, params)
            
            # Atualiza SOAPAction para o método específico
            headers = self.headers.copy()
            headers['SOAPAction'] = f"http://www.cnpm.com.br/{method}"
            
            print(f"🔍 Chamando: {method}")
            print(f"📊 URL: {self.base_url}")
            print(f"📄 SOAPAction: {headers['SOAPAction']}")
            
            # Faz requisição POST SOAP
            response = requests.post(
                self.base_url,
                data=soap_body,
                headers=headers,
                timeout=30
            )
            
            print(f"📊 Status: {response.status_code}")
            print(f"📄 Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                # Parse XML response
                try:
                    root = ET.fromstring(response.text)
                    
                    # Procura por DataSet na estrutura SOAP correta
                    # Estrutura: soap:Envelope -> soap:Body -> methodResponse -> methodResult -> diffgram -> NewDataSet -> Table
                    
                    # Primeiro, procura por diffgram -> NewDataSet
                    diffgram = root.find('.//{urn:schemas-microsoft-com:xml-diffgram-v1}diffgram')
                    if diffgram is not None:
                        new_dataset = diffgram.find('.//NewDataSet')
                        if new_dataset is not None:
                            print("✅ NewDataSet encontrado em diffgram")
                            tables = new_dataset.findall('.//Table')
                            if tables:
                                print(f"   Tables encontradas: {len(tables)}")
                                rows = []
                                
                                for table in tables:
                                    row_data = {}
                                    # Procura por elementos dentro de Table
                                    for elem in table:
                                        # Pula elementos que não são dados
                                        if elem.tag.startswith('{') or elem.tag in ['CODIGO_TIPO_GRUPO', 'DESCRICAO', 'CODIGO_FILIAL_VENDA', 'NOME_FILIAL_VENDA']:
                                            col_name = elem.tag
                                            col_value = elem.text or ''
                                            row_data[col_name] = col_value
                                    
                                    if row_data:  # Só adiciona se encontrou dados
                                        rows.append(row_data)
                                        print(f"     Row extraída: {row_data}")
                                
                                if rows:
                                    print(f"   Rows extraídas: {len(rows)}")
                                    return {"table": "NewDataSet", "data": rows}
                    
                    # Procura por DataSet com namespace
                    dataset = root.find('.//{http://www.cnpm.com.br/}DataSet')
                    if dataset is not None:
                        print("✅ DataSet encontrado com namespace")
                        tables = dataset.findall('.//{http://www.cnpm.com.br/}Table')
                        for table in tables:
                            table_name = table.get('name', 'Table')
                            rows = []
                            
                            for row in table.findall('.//{http://www.cnpm.com.br/}Row'):
                                row_data = {}
                                for col in row.findall('.//{http://www.cnpm.com.br/}Column'):
                                    col_name = col.get('name', '')
                                    col_value = col.text or ''
                                    row_data[col_name] = col_value
                                rows.append(row_data)
                            
                            return {"table": table_name, "data": rows}
                    
                    # Se não encontrou DataSet, procura sem namespace
                    dataset = root.find('.//DataSet')
                    if dataset is not None:
                        print("✅ DataSet encontrado sem namespace")
                        tables = dataset.findall('.//Table')
                        for table in tables:
                            table_name = table.get('name', 'Table')
                            rows = []
                            
                            for row in table.findall('.//Row'):
                                row_data = {}
                                for col in row.findall('.//Column'):
                                    col_name = col.get('name', '')
                                    col_value = col.text or ''
                                    row_data[col_name] = col_value
                                rows.append(row_data)
                            
                            return {"table": table_name, "data": rows}
                    
                    # Se não encontrou DataSet, salva resposta para debug
                    print("⚠️ DataSet não encontrado, salvando resposta para debug...")
                    with open(f"newcon_response_{method}.xml", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"💾 Resposta salva em: newcon_response_{method}.xml")
                    
                    # Lista todas as tags para debug
                    print("🔍 Estrutura da resposta:")
                    for elem in root.iter():
                        print(f"   {elem.tag}")
                    
                    # Se não encontrou DataSet, retorna texto puro
                    return {"text": response.text[:500] + "..." if len(response.text) > 500 else response.text}
                    
                except ET.ParseError as e:
                    print(f"⚠️ Erro no parse XML: {str(e)}")
                    return {"text": response.text[:500] + "..." if len(response.text) > 500 else response.text}
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"📄 Resposta: {response.text[:200]}...")
                return {"error": f"HTTP {response.status_code}", "response": response.text}
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout na requisição")
            return {"error": "Timeout"}
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Erro de conexão: {str(e)}")
            return {"error": f"Erro de conexão: {str(e)}"}
        except Exception as e:
            print(f"❌ Erro na requisição: {str(e)}")
            return {"error": f"Erro na requisição: {str(e)}"}

def test_soap_client():
    """Testa o cliente SOAP"""
    
    print("🧪 Testando Cliente SOAP da Newcon")
    print("=" * 50)
    
    client = NewconSoapClient()
    
    # 1. Teste: Categorias (sem parâmetros)
    print("\n📋 1. Testando cnsTiposGrupos...")
    result = client.call_soap_method("cnsTiposGrupos")
    
    if "data" in result:
        print(f"✅ Sucesso! Encontradas {len(result['data'])} categorias:")
        for cat in result["data"]:
            codigo = cat.get('CODIGO_TIPO_GRUPO', 'N/A')
            descricao = cat.get('DESCRICAO', 'N/A')
            print(f"   - {codigo}: {descricao}")
        
        # 2. Teste: Filiais (sem parâmetros)
        print("\n🏢 2. Testando cnsFiliaisVendas...")
        result_filiais = client.call_soap_method("cnsFiliaisVendas")
        
        if "data" in result_filiais:
            print(f"✅ Sucesso! Encontradas {len(result_filiais['data'])} filiais:")
            for fil in result_filiais["data"]:
                codigo = fil.get('CODIGO_FILIAL_VENDA', 'N/A')
                nome = fil.get('NOME_FILIAL_VENDA', 'N/A')
                print(f"   - {codigo}: {nome}")
            
            # 3. Teste: Tipos de venda (com parâmetro)
            if result["data"]:
                primeira_categoria = result["data"][0].get('CODIGO_TIPO_GRUPO')
                if primeira_categoria:
                    print(f"\n🛒 3. Testando cnsTiposVendas com categoria {primeira_categoria}...")
                    
                    result_tipos = client.call_soap_method("cnsTiposVendas", {
                        "Codigo_Tipo_Grupo": primeira_categoria
                    })
                    
                    if "data" in result_tipos:
                        print(f"✅ Sucesso! Encontrados {len(result_tipos['data'])} tipos de venda:")
                        for tipo in result_tipos["data"]:
                            codigo = tipo.get('Codigo_Tipo_Venda', 'N/A')
                            descricao = tipo.get('Descricao', 'N/A')
                            print(f"   - {codigo}: {descricao}")
                        
                        # 4. Teste: Bens disponíveis (com parâmetros)
                        if result_filiais["data"] and result_tipos["data"]:
                            primeira_filial = result_filiais["data"][0].get('CODIGO_FILIAL_VENDA')
                            primeiro_tipo_venda = result_tipos["data"][0].get('Codigo_Tipo_Venda')
                            
                            print(f"\n💰 4. Testando cnsBensDisponiveis...")
                            print(f"   Filial: {primeira_filial}, Categoria: {primeira_categoria}, TipoVenda: {primeiro_tipo_venda}")
                            
                            result_bens = client.call_soap_method("cnsBensDisponiveis", {
                                "Codigo_Filial": primeira_filial,
                                "Codigo_Tipo_Grupo": primeira_categoria,
                                "Codigo_Tipo_Venda": primeiro_tipo_venda
                            })
                            
                            if "data" in result_bens:
                                print(f"✅ Sucesso! Encontrados {len(result_bens['data'])} bens:")
                                for i, bem in enumerate(result_bens["data"][:3]):  # Mostra apenas os 3 primeiros
                                    codigo = bem.get('Codigo_Bem', 'N/A')
                                    descricao = bem.get('Descricao', 'N/A')
                                    valor = bem.get('Valor_Bem', 'N/A')
                                    print(f"   - {codigo}: {descricao} - R$ {valor}")
                                if len(result_bens["data"]) > 3:
                                    print(f"   ... e mais {len(result_bens['data']) - 3} bens")
                            else:
                                print(f"❌ Erro ao buscar bens: {result_bens}")
                    else:
                        print(f"❌ Erro ao buscar tipos de venda: {result_tipos}")
                else:
                    print("❌ Primeira categoria não tem código válido")
        else:
            print(f"❌ Erro ao buscar filiais: {result_filiais}")
    else:
        print(f"❌ Erro ao buscar categorias: {result}")

if __name__ == "__main__":
    test_soap_client()
