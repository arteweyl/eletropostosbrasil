import os
import csv
import json
import urllib.request
import urllib.parse
import time
import logging
from config import CSV_PATH, CSV_HEADERS, SEARCH_HUBS
from utils import haversine_distance, parse_address_components, normalize_network_name
from compile_data import compile_csv_to_js

logger = logging.getLogger(__name__)

def fetch_google_places_stations(api_key: str, lat: float, lon: float, radius: float) -> list:
    """
    Busca postos de recarga elétrica em um determinado hub geográfico usando a API do Google Places (New v1/places:searchText).
    """
    query = "posto de recarga veiculo eletrico"
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location"
    }
    
    payload = {
        "textQuery": query,
        "languageCode": "pt-BR",
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lon
                },
                "radius": float(radius)
            }
        }
    }
    
    stations = []
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('places', [])
            
            for item in results:
                loc = item.get('location', {})
                glat = loc.get('latitude')
                glon = loc.get('longitude')
                if not glat or not glon:
                    continue
                
                place_id = item.get('id', '')
                displayNameObj = item.get('displayName', {})
                nome = displayNameObj.get('text', 'Eletroposto')
                address = item.get('formattedAddress', '')
                cidade, estado = parse_address_components(address)
                
                # Heurística para operadora com base no nome
                rede = normalize_network_name("Independente", nome)

                stations.append({
                    "id_posto": f"gplaces_{place_id}",
                    "nome": nome,
                    "latitude": float(glat),
                    "longitude": float(glon),
                    "endereco": address.split(' - ')[0] if address else "",
                    "cidade": cidade,
                    "estado": estado,
                    "tipo_conector": "Não Informado",
                    "potencia_kw": "Não Informada",
                    "rede": rede,
                    "preco_recarga": "Não Informado",
                    "status_operacional": "Ativo",
                    "is_publico": True,
                    "fonte_dados": "Google Places"
                })
    except Exception as e:
        logger.error(f"Erro ao buscar na API do Google para ({lat}, {lon}): {e}")
        
    return stations

def run_google_places_crawler(api_key: str = None) -> int:
    """
    Executa a captura da API Google Places, faz a deduplicação espacial e grava na base de dados.
    """
    if not api_key:
        api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
        
    if not api_key:
        logger.error("Chave GOOGLE_PLACES_API_KEY não localizada nas variáveis de ambiente.")
        print("\n[Erro] Defina a chave rodando:")
        print("export GOOGLE_PLACES_API_KEY='sua-chave-aqui'\n")
        return 0

    # 1. Carregar postos existentes para cruzamento/deduplicação
    existing_stations = []
    
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['latitude'] = float(row['latitude'])
                    row['longitude'] = float(row['longitude'])
                    existing_stations.append(row)
            logger.info(f"Carregados {len(existing_stations)} postos existentes do CSV.")
        except Exception as e:
            logger.error(f"Erro ao carregar banco de dados atual: {e}")
    else:
        logger.info("Nenhum banco de dados prévio encontrado. Criando um novo.")

    # 2. Executar busca em cada hub
    google_stations = []
    logger.info(f"Iniciando buscas na API Google Places em {len(SEARCH_HUBS)} hubs metropolitanos...")
    
    for hub in SEARCH_HUBS:
        logger.info(f"• Buscando no hub: {hub['nome']}...")
        results = fetch_google_places_stations(api_key, hub['lat'], hub['lon'], hub['radius'])
        google_stations.extend(results)
        logger.info(f"  Encontrados {len(results)} postos no hub.")
        time.sleep(1) # evita limites de quota imediatos
        
    logger.info(f"Total bruto de postos retornados pelo Google: {len(google_stations)}")

    # 3. Deduplicar contra os dados existentes (limite de 50 metros)
    new_added = 0
    for g_posto in google_stations:
        is_duplicate = False
        
        # Cruzamento espacial para evitar o mesmo ponto físico
        for e_posto in existing_stations:
            dist = haversine_distance(
                g_posto['latitude'], g_posto['longitude'],
                e_posto['latitude'], e_posto['longitude']
            )
            if dist < 50: # Se estiver a menos de 50m, consideramos o mesmo eletroposto
                is_duplicate = True
                # Enriquecer campos vazios do existente com dados do Google
                if not e_posto.get('cidade') and g_posto.get('cidade'):
                    e_posto['cidade'] = g_posto['cidade']
                if not e_posto.get('estado') and g_posto.get('estado'):
                    e_posto['estado'] = g_posto['estado']
                if (not e_posto.get('endereco') or len(e_posto.get('endereco')) < 3) and g_posto.get('endereco'):
                    e_posto['endereco'] = g_posto['endereco']
                break
                
        if not is_duplicate:
            existing_stations.append(g_posto)
            new_added += 1

    logger.info(f"Deduplicação concluída: {new_added} novos postos do Google Places adicionados.")

    # 4. Salvar base unificada
    try:
        with open(CSV_PATH, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(existing_stations)
        logger.info(f"Base de dados consolidada salva em: {CSV_PATH} (Total: {len(existing_stations)} postos).")
    except Exception as e:
        logger.error(f"Erro ao salvar base de dados consolidada: {e}")
        return 0
        
    # 5. Recompilar dados para o JS do painel
    compile_csv_to_js()
    return new_added

if __name__ == "__main__":
    from utils import setup_logging
    setup_logging()
    run_google_places_crawler()
