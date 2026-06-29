# Eletropostos Brasil ⚡

Plataforma colaborativa e mapa interativo de postos de recarga elétrica para veículos elétricos (VE) no Brasil. Este repositório contém o pipeline ETL de coleta, consolidação e enriquecimento de dados geográficos, além do painel de visualização web local.

---

## 📁 Estrutura do Repositório

```text
├── data/
│   ├── eletropostos_brasil.csv   # Banco de dados consolidado principal (CSV)
│   ├── eletropostos_osm.csv      # Backup dos dados puros obtidos via OpenStreetMap
│   └── eletropostos_data.js      # Base compilada em formato JS para consumo do frontend
├── src/
│   ├── config.py                 # Centralização de configurações e hubs de busca
│   ├── utils.py                  # Funções utilitárias (cálculo de distância, parsing de endereços)
│   ├── crawler.py                # Coletor de dados do OpenStreetMap (Overpass API)
│   ├── google_places_crawler.py  # Coletor de dados do Google Places API (New)
│   ├── enrich_data.py            # Enriquecedor de endereços usando OSM Nominatim
│   ├── clean_data.py             # Normalizador e limpador de redes operadoras
│   └── compile_data.py           # Compilador do CSV para eletropostos_data.js
├── tests/
│   └── test_utils.py             # Testes unitários do projeto (cobertura de utilitários)
├── index.html                # Dashboard / Mapa interativo local (Leaflet.js)
├── run_etl.py                # Wrapper CLI central para executar o pipeline
├── run_dashboard.py          # Script para iniciar o servidor web local
├── PLANEJAMENTO.md           # Documento de planejamento e arquitetura do projeto
└── .gitignore                # Arquivos ignorados pelo Git
```

---

## ⚙️ Pré-requisitos

Os scripts foram desenvolvidos utilizando apenas a **biblioteca padrão do Python 3.8+**, eliminando a necessidade de instalar dependências externas via `pip` (como `requests` ou `pandas`). 

---

## 🚀 Como Executar o Pipeline (ETL)

O arquivo `run_etl.py` serve como a interface central de linha de comando para gerenciar as coletas e processamentos de dados.

### 1. Executar o fluxo completo
Para realizar todo o processo (capturar do OpenStreetMap, capturar do Google Places, enriquecer locais ausentes e atualizar o arquivo de dados do painel):

```bash
export GOOGLE_PLACES_API_KEY="sua-chave-api-do-google-aqui"
python3 run_etl.py --all
```

### 2. Executar etapas específicas
Você pode combinar ou isolar as flags dependendo da sua necessidade:

*   **Coletar apenas dados do OpenStreetMap:**
    ```bash
    python3 run_etl.py --osm
    ```
*   **Coletar apenas dados do Google Places (atualizando postos novos e enriquecendo existentes):**
    ```bash
    export GOOGLE_PLACES_API_KEY="sua-chave-api-do-google-aqui"
    python3 run_etl.py --google
    ```
    *(Opcional: Você pode passar a chave diretamente via argumento:* `python3 run_etl.py --google --key "sua-chave"`*)*
*   **Enriquecer endereços vazios:**
    ```bash
    python3 run_etl.py --enrich
    ```
*   **Normalizar nomes das redes operadoras nos arquivos CSV:**
    ```bash
    python3 run_etl.py --clean
    ```
*   **Apenas compilar dados do CSV para JavaScript:**
    ```bash
    python3 run_etl.py --compile
    ```

---

## 🖥️ Como Visualizar no Navegador (Dashboard)

Inicie o servidor de desenvolvimento local para renderizar o mapa do Leaflet.js:

```bash
python3 run_dashboard.py
```

O script iniciará um servidor em `http://localhost:8001` e abrirá a página automaticamente no seu navegador padrão.

---

## 🧪 Testes Unitários

Para garantir a confiabilidade dos cálculos geográficos, extração de endereços e regras de normalização de redes, o repositório possui uma suite de testes unitários escrita com o módulo padrão `unittest` do Python.

Para rodar os testes a partir do diretório raiz do projeto:

```bash
python3 -m unittest tests/test_utils.py
```

---



