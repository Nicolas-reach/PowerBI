# 📊 Nissan Sales AI Dashboard

Um ecossistema de análise de dados de vendas automotivas que une processamento em Python, um backend robusto em Java e relatórios automatizados por Inteligência Artificial, visualizados no Power BI.

## 🎯 Objetivo do Projeto
Transformar dados brutos de vendas das concessionárias Nissan em insights estratégicos. O sistema não apenas gera gráficos, mas utiliza modelos de Linguagem Natural (LLMs) para ler os resultados e redigir relatórios gerenciais automaticamente, apontando tendências de mercado, quedas de desempenho e sugestões de ação.

## 🏗️ Arquitetura e Divisão de Tecnologias

Este projeto foi construído utilizando uma arquitetura de microsserviços para separar responsabilidades:

- **Data Engineering (Python):** Scripts (`gerar_dados.py` e `processar_vendas.py`) responsáveis por simular uma base de dados realista de vendas, tratar os dados e prepará-los para consumo.
- **AI & Backend (Java):** Uma API estruturada que consome a base de dados processada, calcula os KPIs comerciais e integra-se a um LLM para gerar o relatório textual automatizado.
- **Business Intelligence (Power BI):** A interface final que consome os dados e a API, exibindo painéis interativos e o relatório gerado pela IA.

## 📁 Estrutura Atual do Repositório

| Arquivo / Diretório | Descrição |
|---------------------|-----------|
| `/dados` | Diretório onde os arquivos CSV/JSON gerados são armazenados. |
| `gerar_dados.py` | Script para criação da base de dados fictícia de vendas. |
| `processar_vendas.py` | Script de limpeza e estruturação (ETL) dos dados brutos. |
| `requirements.txt` | Lista de dependências e bibliotecas do ambiente Python. |
| `/api-java` | Microsserviço de backend e integração com IA. |

---
*Projeto desenvolvido para demonstração de automação, engenharia de dados e IA.*
