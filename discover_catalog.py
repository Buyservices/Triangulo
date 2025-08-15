#!/usr/bin/env python3
"""
Script para descobrir dados reais do catálogo da Newcon
Chama os WebServices diretamente para obter códigos válidos
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
import json

BASE_URL = "https://webatendimento.consorciotriangulo.com.br/wsregvenda/wsRegVenda.asmx"


def call_newcon_webservice(method: str, params: Dict[str, str] = None) -> Dict[str, Any]:
    """Chama WebService da Newcon diretamente"""
    try:
        url = f"{BASE_URL}/{method}"
        print(f"🔍 Chamando: {url}")
        
        if params:
            response = requests.get(url, params=params, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            # Parse XML response
            try:
                root = ET.fromstring(response.text)
                
                # Procura por DataSet com namespace correto
                dataset = root.find('.//{http://www.cnpm.com.br/}DataSet')
                if dataset is not None:
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


def discover_catalog() -> Dict[str, Any]:
    """Descobre o catálogo completo em cascata"""
    print("🚀 Iniciando descoberta do catálogo da Newcon")
    print("=" * 60)

    catalog = {}

    # 1. Categorias (Tipos de Grupo)
    print("\n📋 1. Descobrindo categorias...")
    categorias = call_newcon_webservice("cnsTiposGrupos")
    print(f"📊 Resultado categorias: {categorias}")

    if "data" in categorias:
        catalog["categorias"] = categorias["data"]
        print(f"✅ Encontradas {len(categorias['data'])} categorias")

        # Mostra as categorias encontradas
        for cat in categorias["data"]:
            print(
                f"   - {cat.get('Codigo_Tipo_Grupo', 'N/A')}: {cat.get('Descricao', 'N/A')}"
            )
    else:
        print(f"❌ Erro ao buscar categorias: {categorias}")
        return catalog

    # 2. Filiais
    print("\n🏢 2. Descobrindo filiais...")
    filiais = call_newcon_webservice("cnsFiliaisVendas")
    print(f"📊 Resultado filiais: {filiais}")

    if "data" in filiais:
        catalog["filiais"] = filiais["data"]
        print(f"✅ Encontradas {len(filiais['data'])} filiais")

        # Mostra as filiais encontradas
        for fil in filiais["data"]:
            print(
                f"   - {fil.get('Codigo_Filial_Venda', 'N/A')}: {fil.get('Nome_Filial_Venda', 'N/A')}"
            )
    else:
        print(f"❌ Erro ao buscar filiais: {filiais}")
        return catalog

    # 3. Para cada categoria, buscar tipos de venda
    print("\n🛒 3. Descobrindo tipos de venda por categoria...")
    catalog["tipos_venda"] = {}

    for categoria in categorias["data"]:
        codigo_tipo_grupo = categoria.get("Codigo_Tipo_Grupo")
        if codigo_tipo_grupo:
            print(
                f"   🔍 Buscando tipos de venda para categoria {codigo_tipo_grupo}..."
            )

            tipos_venda = call_newcon_webservice(
                "cnsTiposVendas", {"Codigo_Tipo_Grupo": codigo_tipo_grupo}
            )

            if "data" in tipos_venda:
                catalog["tipos_venda"][codigo_tipo_grupo] = tipos_venda["data"]
                print(f"      ✅ Encontrados {len(tipos_venda['data'])} tipos de venda")

                # Mostra os tipos de venda encontrados
                for tipo in tipos_venda["data"]:
                    print(
                        f"         - {tipo.get('Codigo_Tipo_Venda', 'N/A')}: {tipo.get('Descricao', 'N/A')}"
                    )
            else:
                print(f"      ❌ Erro ao buscar tipos de venda: {tipos_venda}")

    # 4. Para cada combinação válida, buscar bens disponíveis
    print("\n💰 4. Descobrindo bens disponíveis...")
    catalog["bens"] = {}

    # Pega a primeira filial e primeira categoria para teste
    if filiais["data"] and categorias["data"]:
        filial_teste = filiais["data"][0].get("Codigo_Filial_Venda")
        categoria_teste = categorias["data"][0].get("Codigo_Tipo_Grupo")

        if (
            filial_teste
            and categoria_teste
            and categoria_teste in catalog["tipos_venda"]
        ):
            tipos_venda_categoria = catalog["tipos_venda"][categoria_teste]

            if tipos_venda_categoria:
                tipo_venda_teste = tipos_venda_categoria[0].get("Codigo_Tipo_Venda")

                if tipo_venda_teste:
                    print(
                        f"   🔍 Testando: Filial={filial_teste}, Categoria={categoria_teste}, TipoVenda={tipo_venda_teste}"
                    )

                    bens = call_newcon_webservice(
                        "cnsBensDisponiveis",
                        {
                            "Codigo_Filial": filial_teste,
                            "Codigo_Tipo_Grupo": categoria_teste,
                            "Codigo_Tipo_Venda": tipo_venda_teste,
                        },
                    )

                    if "data" in bens:
                        catalog["bens"][
                            f"{filial_teste}_{categoria_teste}_{tipo_venda_teste}"
                        ] = bens["data"]
                        print(f"      ✅ Encontrados {len(bens['data'])} bens")

                        # Mostra os primeiros bens encontrados
                        for i, bem in enumerate(
                            bens["data"][:3]
                        ):  # Mostra apenas os 3 primeiros
                            print(
                                f"         - {bem.get('Codigo_Bem', 'N/A')}: {bem.get('Descricao', 'N/A')} - R$ {bem.get('Valor_Bem', 'N/A')}"
                            )
                        if len(bens["data"]) > 3:
                            print(f"         ... e mais {len(bens['data']) - 3} bens")
                    else:
                        print(f"      ❌ Erro ao buscar bens: {bens}")

    print("\n" + "=" * 60)
    print("🏁 Descoberta concluída!")

    return catalog


def save_catalog_to_file(
    catalog: Dict[str, Any], filename: str = "catalog_discovered.json"
):
    """Salva o catálogo descoberto em arquivo JSON"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"💾 Catálogo salvo em: {filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {str(e)}")


def print_summary(catalog: Dict[str, Any]):
    """Imprime resumo do catálogo descoberto"""
    print("\n📊 RESUMO DO CATÁLOGO DESCOBERTO")
    print("=" * 60)

    if "categorias" in catalog:
        print(f"📋 Categorias: {len(catalog['categorias'])}")

    if "filiais" in catalog:
        print(f"🏢 Filiais: {len(catalog['filiais'])}")

    if "tipos_venda" in catalog:
        total_tipos = sum(len(tipos) for tipos in catalog["tipos_venda"].values())
        print(f"🛒 Tipos de Venda: {total_tipos} (distribuídos por categoria)")

    if "bens" in catalog:
        total_bens = sum(len(bens) for bens in catalog["bens"].values())
        print(f"💰 Bens Disponíveis: {total_bens} (distribuídos por combinação)")

    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Use os códigos descobertos para testar nossa API")
    print("2. Ajuste os parâmetros nos endpoints da nossa API")
    print("3. Teste cada endpoint com dados reais")


if __name__ == "__main__":
    # Descobre o catálogo
    catalog = discover_catalog()

    if catalog:
        # Salva em arquivo
        save_catalog_to_file(catalog)

        # Imprime resumo
        print_summary(catalog)

        # Mostra exemplo de uso na nossa API
        print("\n🔗 EXEMPLO DE USO NA NOSSA API:")
        if "categorias" in catalog and catalog["categorias"]:
            primeira_categoria = catalog["categorias"][0].get(
                "Codigo_Tipo_Grupo", "N/A"
            )
            print(
                f"GET http://localhost:8000/v1/catalog/sale-types?tipo_grupo={primeira_categoria}"
            )

        if (
            "filiais" in catalog
            and "categorias" in catalog
            and catalog["filiais"]
            and catalog["categorias"]
        ):
            primeira_filial = catalog["filiais"][0].get("Codigo_Filial_Venda", "N/A")
            primeira_categoria = catalog["categorias"][0].get(
                "Codigo_Tipo_Grupo", "N/A"
            )
            if (
                primeira_categoria in catalog.get("tipos_venda", {})
                and catalog["tipos_venda"][primeira_categoria]
            ):
                primeiro_tipo_venda = catalog["tipos_venda"][primeira_categoria][0].get(
                    "Codigo_Tipo_Venda", "N/A"
                )
                print(
                    f"GET http://localhost:8000/v1/catalog/items?filial={primeira_filial}&tipo_grupo={primeira_categoria}&tipo_venda={primeiro_tipo_venda}"
                )
    else:
        print("❌ Falha na descoberta do catálogo")
