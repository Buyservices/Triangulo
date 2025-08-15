# 🏗️ **API de Catálogo de Consórcios - Newcon**

## 📋 **Visão Geral**

Esta API implementa o **fluxo completo de catálogo de cartas de crédito/consórcio** da Newcon, expondo endpoints REST que internamente chamam os WebServices SOAP da empresa.

## 🎯 **Funcionalidades Implementadas**

### ✅ **Endpoints Disponíveis**

| Endpoint                 | Método | Descrição                    | WebService Newcon      |
| ------------------------ | ------ | ---------------------------- | ---------------------- |
| `/v1/catalog/categories` | GET    | Categorias de consórcio      | `cnsTiposGrupos`       |
| `/v1/catalog/filiais`    | GET    | Filiais de venda             | `cnsFiliaisVendas`     |
| `/v1/catalog/sale-types` | GET    | Tipos de venda por categoria | `cnsTiposVendas`       |
| `/v1/catalog/items`      | GET    | Bens disponíveis             | `cnsBensDisponiveis`   |
| `/v1/catalog/options`    | GET    | Opções comerciais            | `cnsPrazosDisponiveis` |
| `/v1/catalog/rules`      | GET    | Regras de cobrança           | `cnsRegraCobranca`     |

---

## 🚀 **Como Usar**

### **1. Consultar Categorias**

```http
GET /v1/catalog/categories
```

**Resposta:**

```json
{
  "sucesso": true,
  "mensagem": "Encontradas 3 categorias",
  "categorias": [
    {
      "codigo": "IM",
      "descricao": "Imóveis"
    },
    {
      "codigo": "VE",
      "descricao": "Veículos"
    },
    {
      "codigo": "MO",
      "descricao": "Motocicletas"
    }
  ]
}
```

### **2. Consultar Filiais**

```http
GET /v1/catalog/filiais
```

**Resposta:**

```json
{
  "sucesso": true,
  "mensagem": "Encontradas 5 filiais",
  "filiais": [
    {
      "codigo": "001",
      "nome": "Filial São Paulo"
    },
    {
      "codigo": "002",
      "nome": "Filial Rio de Janeiro"
    }
  ]
}
```

### **3. Consultar Tipos de Venda**

```http
GET /v1/catalog/sale-types?tipo_grupo=IM
```

**Resposta:**

```json
{
  "sucesso": true,
  "mensagem": "Encontrados 2 tipos de venda para categoria IM",
  "tipos_venda": [
    {
      "codigo": "10",
      "descricao": "Venda Direta"
    },
    {
      "codigo": "20",
      "descricao": "Venda com Financiamento"
    }
  ]
}
```

### **4. Consultar Bens Disponíveis**

```http
GET /v1/catalog/items?filial=001&tipo_grupo=IM&tipo_venda=10
```

**Resposta:**

```json
{
  "sucesso": true,
  "mensagem": "Encontrados 15 bens disponíveis",
  "bens": [
    {
      "codigo": "123",
      "descricao": "Apartamento 2 quartos",
      "valor": 250000.0
    },
    {
      "codigo": "124",
      "descricao": "Casa 3 quartos",
      "valor": 350000.0
    }
  ]
}
```

### **5. Consultar Opções Comerciais**

```http
GET /v1/catalog/options?unidade=001&tipo_grupo=IM&representante=000001&filial=001&pessoa=F&situacao_grupo=A
```

**Resposta:**

```json
{
  "sucesso": true,
  "mensagem": "Encontrados 8 prazos disponíveis",
  "prazos": [
    {
      "codigo_grupo": "G001",
      "prazo_venda": 120,
      "valor_prestacao": 2500.0,
      "codigo_bem": "123",
      "valor_bem": 250000.0,
      "codigo_plano": "7",
      "sequencia_agrupamento": "456",
      "percentual_taxa_adm": 10.0,
      "percentual_fundo_reserva": 2.0,
      "data_proxima_assembleia": "15/12/2024",
      "cotas_vagas": 45,
      "data_vencimento_limite": "31/12/2024"
    }
  ]
}
```

### **6. Consultar Regras de Cobrança**

```http
GET /v1/catalog/rules?plano=7&prazo=120&seq=456&tipo_grupo=IM&tipo_venda=10&bem=123&filial=001&rateia=N&numAssem=45
```

**Resposta:**

```json
{
  "codigo_plano": "7",
  "prazo": 120,
  "sequencia_agrupamento": "456",
  "faixas_parcelas": [
    {
      "faixa_inicial": 1,
      "faixa_final": 12,
      "percentual_fundo_comum": 88.0,
      "percentual_taxa_adm": 10.0,
      "percentual_fundo_reserva": 2.0,
      "percentual_seguros": 0.0,
      "valor_parcela": 2500.0
    },
    {
      "faixa_inicial": 13,
      "faixa_final": 120,
      "percentual_fundo_comum": 90.0,
      "percentual_taxa_adm": 8.0,
      "percentual_fundo_reserva": 2.0,
      "percentual_seguros": 0.0,
      "valor_parcela": 2400.0
    }
  ]
}
```

---

## 🔧 **Arquitetura Técnica**

### **Fluxo de Dados**

```
HTTP Request → Controllers → Use Cases → Domain → Infrastructure → Newcon SOAP
```

### **Camadas Implementadas**

1. **Domain**: Entidades de negócio (TipoGrupo, FilialVenda, etc.)
2. **Application**: Casos de uso e DTOs
3. **Infrastructure**: Cliente SOAP e repositório Newcon
4. **Interfaces**: Controllers, schemas e routers

### **WebServices SOAP Utilizados**

- **`cnsTiposGrupos`**: Categorias de consórcio
- **`cnsFiliaisVendas`**: Filiais disponíveis
- **`cnsTiposVendas`**: Tipos de venda por categoria
- **`cnsBensDisponiveis`**: Bens/cartas disponíveis
- **`cnsPrazosDisponiveis`**: Opções comerciais
- **`cnsRegraCobranca`**: Composição da parcela

---

## 📊 **Parâmetros Importantes**

### **Situação do Grupo**

- **A**: Ativo (aceitando propostas)
- **F**: Fechado (não aceita propostas)
- **X**: Cancelado

### **Tipo de Pessoa**

- **F**: Física
- **J**: Jurídica

### **Ordem de Pesquisa**

- **G**: Por Grupo
- **P**: Por Prazo

### **Rateia**

- **S**: Sim (rateia entre grupos)
- **N**: Não (não rateia)

---

## 🚨 **Tratamento de Erros**

### **Erros HTTP**

- **400**: Parâmetros inválidos
- **500**: Erro interno ou erro da Newcon

### **Erros Newcon**

- Parâmetros obrigatórios ausentes
- Validações de negócio
- Erros de sistema

### **Resposta de Erro**

```json
{
  "sucesso": false,
  "mensagem": "Erro ao consultar categorias",
  "categorias": [],
  "erro": "Parâmetro ausente: Codigo_Tipo_Grupo"
}
```

---

## 🔍 **Debug e Logs**

### **Logs de Integração**

- Todas as chamadas SOAP são logadas
- Respostas XML são capturadas
- Erros são detalhados com contexto

### **Monitoramento**

- Status HTTP das chamadas SOAP
- Tempo de resposta
- Taxa de sucesso/erro

---

## 📈 **Performance e Cache**

### **Recomendações**

- **Cache estático**: Categorias, filiais e tipos de venda
- **Cache dinâmico**: Prazos e opções (revalidar a cada consulta)
- **Timeout**: 30 segundos para chamadas SOAP

### **Otimizações**

- Chamadas assíncronas
- Parse eficiente de XML
- Tratamento de erros sem retry automático

---

## 🧪 **Testes**

### **Endpoints de Teste**

```bash
# Testar categorias
curl "http://localhost:8000/v1/catalog/categories"

# Testar filiais
curl "http://localhost:8000/v1/catalog/filiais"

# Testar tipos de venda
curl "http://localhost:8000/v1/catalog/sale-types?tipo_grupo=IM"
```

### **Validação**

- Schemas Pydantic validam entrada/saída
- Tratamento de erros robusto
- Logs detalhados para debug

---

## 🚀 **Próximos Passos**

### **Funcionalidades Planejadas**

- [ ] Cache Redis para melhorar performance
- [ ] Rate limiting para proteger a API
- [ ] Métricas de uso e performance
- [ ] Documentação OpenAPI/Swagger
- [ ] Testes automatizados

### **Melhorias Técnicas**

- [ ] Circuit breaker para resiliência
- [ ] Retry automático para falhas temporárias
- [ ] Compressão de respostas
- [ ] Paginação para grandes volumes

---

## 🏆 **Status**

**✅ IMPLEMENTADO**: API completa de catálogo funcionando
**✅ TESTADO**: Endpoints validados com Newcon
**✅ PRODUÇÃO**: Pronto para uso em ambiente produtivo
**🔄 EVOLUÇÃO**: Novas funcionalidades em desenvolvimento
