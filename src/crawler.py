import json
import urllib.request
import csv
import os
import logging
from config import CSV_PATH, CSV_HEADERS
from utils import normalize_network_name

logger = logging.getLogger(__name__)

def fetch_osm_charging_stations() -> list:
    """
    Busca pontos de recarga veicular no Brasil usando a API Overpass do OpenStreetMap.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = """
    [out:json][timeout:180];
    area["ISO3166-1"="BR"]->.searchArea;
    (
      node["amenity"="charging_station"](area.searchArea);
      way["amenity"="charging_station"](area.searchArea);
    );
    out center;
    """
    
    req = urllib.request.Request(
        overpass_url, 
        data=query.encode('utf-8'), 
        headers={'User-Agent': 'EletropostosBrasilCrawler/1.0'}
    )
    
    logger.info("Buscando dados no OpenStreetMap (Overpass API)...")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('elements', [])
    except Exception as e:
        logger.error(f"Erro ao buscar dados no OpenStreetMap: {e}")
        return []

def run_osm_crawler() -> int:
    """
    Executa a captura dos dados do OSM e grava no arquivo CSV principal.
    """
    elements = fetch_osm_charging_stations()
    if not elements:
        logger.warning("Nenhum dado encontrado no OpenStreetMap ou falha na requisição.")
        return 0
        
    logger.info(f"Encontrados {len(elements)} elementos no OSM. Tratando dados...")
    
    count = 0
    try:
        with open(CSV_PATH, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
            
            for elem in elements:
                tags = elem.get('tags', {})
                
                # Determinar coordenadas
                lat = elem.get('lat') or elem.get('center', {}).get('lat')
                lon = elem.get('lon') or elem.get('center', {}).get('lon')
                if not lat or not lon:
                    continue
                    
                # Extrair atributos
                id_posto = f"osm_{elem.get('id')}"
                nome = tags.get('name') or tags.get('operator') or f"Eletroposto {tags.get('brand', 'Independente')}"
                
                # Endereço completo a partir de tags OSM
                addr_street = tags.get('addr:street', '')
                addr_num = tags.get('addr:housenumber', '')
                addr_city = tags.get('addr:city', '')
                addr_state = tags.get('addr:state', '')
                
                endereco = f"{addr_street} {addr_num}".strip()
                cidade = addr_city or tags.get('is_in:city', '')
                estado = addr_state or tags.get('is_in:state', '')
                
                # Traduzir tipos de conector
                tipo_conector = []
                if tags.get('socket:type2') or tags.get('socket:type2:output') or tags.get('socket:type2_cable'):
                    tipo_conector.append("Type 2")
                if tags.get('socket:ccs') or tags.get('socket:ccs:output') or tags.get('socket:ccs_cable'):
                    tipo_conector.append("CCS2")
                if tags.get('socket:chademo') or tags.get('socket:chademo:output'):
                    tipo_conector.append("CHAdeMO")
                if not tipo_conector:
                    tipo_conector.append("Não Informado")
                    
                potencia_kw = tags.get('power', 'Não Informada')
                raw_rede = tags.get('operator') or tags.get('brand') or "Independente"
                rede = normalize_network_name(raw_rede, nome)
                preco_recarga = tags.get('fee') or "Não Informado"
                
                # Escrever linha no formato padronizado
                writer.writerow([
                    id_posto, nome, lat, lon, endereco, cidade, estado, 
                    ", ".join(tipo_conector), potencia_kw, rede, 
                    preco_recarga, "Ativo", True, "OpenStreetMap"
                ])
                count += 1
                
        logger.info(f"Salvo com sucesso {count} registros em {CSV_PATH}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo de saída do OSM: {e}")
        
    return count

if __name__ == "__main__":
    from utils import setup_logging
    setup_logging()
    run_osm_crawler()
