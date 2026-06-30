# Proposta de Serviço de Dados: Agregador Eletropostos Brasil

**Base dos Dados (BD)**  
**Data:** 29 de Junho de 2026  

---

## 1. Resumo Executivo

O avanço da eletromobilidade no Brasil carece de uma base de dados unificada, padronizada e aberta sobre a infraestrutura de recarga elétrica. Atualmente, os dados estão fragmentados entre múltiplas redes operadoras e registros incompletos.

Esta proposta detalha a estruturação do projeto **Eletropostos Brasil** para o ambiente da **Base dos Dados (GCP/BigQuery)**, evoluindo a Prova de Conceito (POC) de viabilidade técnica já realizada. O objetivo é consolidar o primeiro repositório nacional de dados abertos de eletropostos, servindo de base para tomadas de decisão estratégica em planejamento de infraestrutura urbana e transição energética.

---

## 2. Status Atual & Viabilidade Técnica (POC)

Concluímos com sucesso a validação técnica da extração e consolidação dos dados locais com o script ETL do pipeline. Os dados iniciais foram validados espacialmente e estruturados em 4 commits de boas práticas de engenharia de software:

*   **Deduplicação Espacial:** Implementada via algoritmo Haversine, unificando registros distantes a menos de 50 metros.
*   **Normalização de Redes:** Unificação de grafias erradas de operadoras (ex: *chell* ➔ *Shell Recharge*, *BR* ➔ *Petrobras*).
*   **Enriquecimento Geográfico:** Geocodificação reversa de endereços ausentes via OpenStreetMap Nominatim.

---

## 3. Fontes de Dados Mapeadas (Fase 1)

O projeto consolida três grandes fontes complementares na **Fase 1**:

| Fonte | Tipo | Cobertura / Benefício | Status no Projeto |
| :--- | :--- | :--- | :--- |
| **OpenStreetMap (OSM)** | Pública (Overpass API) | Excelente cobertura espacial inicial e metadados de acesso (público/privado). | **100% Implementado** |
| **Google Places API** | Proprietária (v1 SearchText) | Enriquecimento crítico de horários de funcionamento, nomes comerciais de redes e dados de localização adicionais. | **100% Implementado** |
| **Open Charge Map (OCM)** | Pública (API REST) | Dados específicos de veículos elétricos (potência exata em kW, tipos detalhados de conectores e feedback de usuários). | **Pendente de Integração** |

---

## 4. Divisão de Fases do Projeto

O projeto está dividido em fases incrementais, da engenharia de dados à disponibilização em tempo real:

### 📂 Fase 1: Ingestão de Dados & Infraestrutura de Staging (GCP / BigQuery)
*   **Engenharia de Dados:** Desenvolvimento do script de carregamento final (`src/upload_bigquery.py`) para criar o dataset e fazer o upload do CSV consolidado no BigQuery.
*   **Integração do OCM:** Desenvolvimento do crawler da terceira fonte de dados (Open Charge Map) para complementar metadados técnicos.
*   **Modelo de Dados BD:** Criação do esquema definitivo no BigQuery (`eletropostos_brasil.eletropostos_consolidado`) com metadados documentados.
*   **Fluxo Colaborativo Staging:** Integração de uma planilha externa do Google Sheets (conectada a um formulário público de sugestões) diretamente como tabela de staging no BigQuery para aprovação rápida por moderadores.
*   **Prazo estimado:** 2 semanas.

### 📊 Fase 2: Visualização & Analytics (Looker Studio)
*   **Métricas de Negócio:** Criação de um painel de inteligência de mercado conectado diretamente à tabela consolidada do BigQuery.
*   **Visualização Analítica:** Dashboards de distribuição de postos por estado, potência média por rede operadora, conexões por tipo de plugue e crescimento da infraestrutura.
*   **Prazo estimado:** 1 semana.

### 🌐 Fase 3: Dashboard Web Interativo (Aplicação Frontend)
*   **Interface BD:** Criação do site público utilizando Next.js e Leaflet/Mapbox (estilo Base dos Dados).
*   **Desempenho:** Renderização estática com buscas espaciais otimizadas e carregamento em milissegundos para os usuários finais.
*   **Prazo estimado:** 3 semanas.

### ⚡ Fase 4: Integração de APIs Comerciais & Tempo Real (OCPI/OCPP)
*   **Status Online:** Conectar a base consolidada do BigQuery aos barramentos privados de operadoras (EZVolt, Tupi, Raízen) via protocolo **OCPI** para exibir disponibilidade em tempo real.
*   **Prazo estimado:** A definir (depende de acordos e chaves de acesso privadas das operadoras).

---

## 5. Orçamento & Custos Estimados (GCP)

Seguindo a tabela padrão de consumo da Base dos Dados, os custos estimados de processamento em nuvem são extremamente baixos devido ao baixo volume inicial (KB/MB):

| Recurso | Função | Plano Recomendado | Custo Estimado (Mensal) |
| :--- | :--- | :--- | :--- |
| **GCP BigQuery** | Armazenamento e Processamento | BigQuery On-Demand | Gratuito (abaixo de 10GB de storage e 1TB de processamento/mês) |
| **GCP Cloud Storage** | Armazenamento de backups frios | Standard Storage | R$ 0,00 (dentro da camada gratuita do GCP) |
| **Github Actions** | CI/CD e orquestração do pipeline | Runners Públicos | Gratuito para repositórios públicos |
