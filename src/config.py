import os

# Configuração de Caminhos
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Garante que a pasta data exista
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, "eletropostos_brasil.csv")
OSM_CSV_PATH = os.path.join(DATA_DIR, "eletropostos_osm.csv")
JS_PATH = os.path.join(DATA_DIR, "eletropostos_data.js")

# Configuração da Porta do Dashboard
DASHBOARD_PORT = 8001

# Hubs Metropolitanos para Busca (Google Places API)
SEARCH_HUBS = [
    {"nome": "São Paulo - SP", "lat": -23.5615, "lon": -46.6560, "radius": 50000},
    {"nome": "Rio de Janeiro - RJ", "lat": -22.9068, "lon": -43.1729, "radius": 40000},
    {"nome": "Belo Horizonte - MG", "lat": -19.9167, "lon": -43.9345, "radius": 30000},
    {"nome": "Curitiba - PR", "lat": -25.4290, "lon": -49.2671, "radius": 30000},
    {"nome": "Porto Alegre - RS", "lat": -30.0346, "lon": -51.2177, "radius": 30000},
    {"nome": "Campinas - SP", "lat": -22.9056, "lon": -47.0608, "radius": 25000},
    {"nome": "Brasília - DF", "lat": -15.7942, "lon": -47.8822, "radius": 35000},
    {"nome": "Florianópolis - SC", "lat": -27.5954, "lon": -48.5480, "radius": 20000},
    {"nome": "Goiânia - GO", "lat": -16.6869, "lon": -49.2648, "radius": 25000},
    {"nome": "Salvador - BA", "lat": -12.9777, "lon": -38.5016, "radius": 25000},
    {"nome": "Recife - PE", "lat": -8.0578, "lon": -34.8829, "radius": 25000},
    {"nome": "Fortaleza - CE", "lat": -3.7319, "lon": -38.5267, "radius": 25000}
]

# Tradução de Estado por Extenso para UF
STATE_MAP = {
    "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM", "Bahia": "BA",
    "Ceará": "CE", "Distrito Federal": "DF", "Espírito Santo": "ES", "Goiás": "GO",
    "Maranhão": "MA", "Mato Grosso": "MT", "Mato Grosso do Sul": "MS", "Minas Gerais": "MG",
    "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE", "Piauí": "PI",
    "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN", "Rio Grande do Sul": "RS",
    "Rondônia": "RO", "Roraima": "RR", "Santa Catarina": "SC", "São Paulo": "SP",
    "Sergipe": "SE", "Tocantins": "TO"
}

# Cabeçalhos Padrão do Dicionário de Dados
CSV_HEADERS = [
    "id_posto", "nome", "latitude", "longitude", "endereco", 
    "cidade", "estado", "tipo_conector", "potencia_kw", "rede", 
    "preco_recarga", "status_operacional", "is_publico", "fonte_dados"
]
