import csv
import json
import urllib.request
import time
import os
import logging
from config import CSV_PATH, STATE_MAP
from compile_data import compile_csv_to_js

logger = logging.getLogger(__name__)

def reverse_geocode(lat: float, lon: float) -> tuple[dict, str]:
    """
    Realiza geocodificação reversa usando a API pública do Nominatim (OpenStreetMap).
    Retorna uma tupla (detalhes_do_endereco, nome_exibicao).
    """
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'EletropostosBrasilEnricher/1.0 (arteweyl@gmail.com)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            addr_details = res_data.get('address', {})
            display_name = res_data.get('display_name', '')
            return addr_details, display_name
    except Exception as e:
        logger.warning(f"Falha ao geocodificar ({lat}, {lon}): {e}")
        return {}, ""

def run_enrichment() -> int:
    """
    Itera sobre o banco de dados CSV, identifica registros sem dados de endereço ou localização
    e executa geocodificação reversa para enriquecer a base.
    """
    if not os.path.exists(CSV_PATH):
        logger.error(f"Arquivo CSV não encontrado em: {CSV_PATH}")
        return 0

    # Carregar linhas do CSV
    rows = []
    try:
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)
    except Exception as e:
        logger.error(f"Erro ao ler banco de dados para enriquecimento: {e}")
        return 0

    total_rows = len(rows)
    logger.info(f"Iniciando enriquecimento de {total_rows} eletropostos...")
    logger.info("Aguarde, respeitando a política de uso do Nominatim (1 req/seg)...")

    success_count = 0
    start_time = time.time()

    for idx, row in enumerate(rows):
        lat = row.get('latitude')
        lon = row.get('longitude')
        
        if not lat or lon is None:
            continue

        # Pular se o registro já possui endereço, cidade e estado preenchidos
        if row.get('endereco') and row.get('cidade') and row.get('estado'):
            continue

        logger.info(f"Enriquecendo registro {idx + 1}/{total_rows}: {row.get('nome') or 'Sem Nome'} ({lat}, {lon})")

        addr_details, display_name = reverse_geocode(lat, lon)
        
        if addr_details:
            # Identificar cidade
            cidade = (
                addr_details.get('city') or 
                addr_details.get('town') or 
                addr_details.get('suburb') or 
                addr_details.get('municipality') or 
                addr_details.get('village') or 
                addr_details.get('city_district') or
                ""
            )
            
            # Identificar estado (UF)
            state_long = addr_details.get('state', '')
            estado = STATE_MAP.get(state_long, state_long) # Converte para UF, ex: "São Paulo" -> "SP"
            
            # Identificar endereço
            road = addr_details.get('road', '')
            house_num = addr_details.get('house_number', '')
            
            if road:
                endereco = f"{road}, {house_num}".strip(", ")
            else:
                endereco = display_name.split(',')[0] if display_name else ""

            # Alimentar de volta no dicionário do registro
            row['endereco'] = endereco
            row['cidade'] = cidade
            row['estado'] = estado
            success_count += 1
            
            # Delay de 1.1s para respeitar estritamente o limite do Nominatim e evitar ban de IP
            time.sleep(1.1)

    logger.info(f"Geocodificação concluída! {success_count} registros enriquecidos.")

    # Sobrescrever o CSV original com os novos dados
    try:
        with open(CSV_PATH, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"Dados salvos com sucesso em: {CSV_PATH}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo CSV enriquecido: {e}")
        return 0

    # Recompilar os dados para o JS lido pelo painel
    compile_csv_to_js()
    
    elapsed_time = time.time() - start_time
    logger.info(f"Tempo total de execução: {elapsed_time/60:.2f} minutos.")
    return success_count

if __name__ == "__main__":
    from utils import setup_logging
    setup_logging()
    run_enrichment()
