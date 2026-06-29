import csv
import json
import os
import logging
from config import CSV_PATH, JS_PATH

logger = logging.getLogger(__name__)

def compile_csv_to_js() -> bool:
    """
    Lê o arquivo CSV consolidado e compila os registros para um arquivo JavaScript
    que define a variável window.eletropostosData de forma a ser lida pelo dashboard Leaflet.
    """
    if not os.path.exists(CSV_PATH):
        logger.error(f"Arquivo CSV não encontrado em: {CSV_PATH}")
        return False
        
    eletropostos = []
    try:
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Converter tipos numéricos para latitude e longitude
                try:
                    row['latitude'] = float(row['latitude'])
                    row['longitude'] = float(row['longitude'])
                except ValueError:
                    continue
                    
                eletropostos.append(row)
    except Exception as e:
        logger.error(f"Erro ao ler o CSV consolidado: {e}")
        return False
            
    try:
        with open(JS_PATH, mode='w', encoding='utf-8') as f:
            f.write("// Dados compilados dos eletropostos para o dashboard\n")
            f.write("window.eletropostosData = ")
            f.write(json.dumps(eletropostos, ensure_ascii=False, indent=2))
            f.write(";\n")
        logger.info(f"Sucesso: {len(eletropostos)} registros compilados para {JS_PATH}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo compilado JS: {e}")
        return False

if __name__ == "__main__":
    from utils import setup_logging
    setup_logging()
    compile_csv_to_js()
