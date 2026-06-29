import csv
import os
import sys
import logging

# Adiciona o diretório src ao sys.path se necessário
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)

from config import CSV_PATH, OSM_CSV_PATH, CSV_HEADERS
from utils import normalize_network_name, setup_logging
from compile_data import compile_csv_to_js

logger = logging.getLogger("clean_data")

def clean_csv(path: str):
    """Lê um arquivo CSV, normaliza a coluna 'rede' e salva de volta."""
    if not os.path.exists(path):
        logger.warning(f"Arquivo não localizado para limpeza: {path}")
        return
        
    rows = []
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normaliza o nome da rede operadora
                old_rede = row.get('rede', '')
                new_rede = normalize_network_name(old_rede, row.get('nome', ''))
                
                if old_rede != new_rede:
                    logger.debug(f"Normalizado: '{old_rede}' -> '{new_rede}' (Posto: {row.get('nome')})")
                    
                row['rede'] = new_rede
                rows.append(row)
                
        with open(path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(rows)
            
        logger.info(f"Limpeza concluída para {path}. Total de registros: {len(rows)}")
    except Exception as e:
        logger.error(f"Erro ao processar limpeza no arquivo {path}: {e}")

def main():
    setup_logging()
    logger.info("=== Iniciando limpeza e normalização das redes operadoras ===")
    
    # Limpar as duas bases
    clean_csv(CSV_PATH)
    clean_csv(OSM_CSV_PATH)
    
    # Recompilar
    logger.info("Recompilando dados JS do dashboard...")
    compile_csv_to_js()
    
    logger.info("=== Processo de limpeza concluído com sucesso! ===")

if __name__ == "__main__":
    main()
