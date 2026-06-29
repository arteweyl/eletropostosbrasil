import argparse
import sys
import os
import logging

# Adiciona o diretório src/ ao sys.path para permitir importações diretas
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from utils import setup_logging
from crawler import run_osm_crawler
from google_places_crawler import run_google_places_crawler
from enrich_data import run_enrichment
from compile_data import compile_csv_to_js
from clean_data import clean_csv

logger = logging.getLogger("run_etl")

def main():
    parser = argparse.ArgumentParser(
        description="Eletropostos Brasil ETL Pipeline - Coleta, Enriquecimento e Processamento de Dados.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Executar o fluxo completo (OSM -> Google -> Enriquecer -> Compilar)
  python run_etl.py --all

  # Capturar apenas dados do OpenStreetMap
  python run_etl.py --osm

  # Capturar dados do Google Places (requer GOOGLE_PLACES_API_KEY no ambiente)
  export GOOGLE_PLACES_API_KEY='sua-chave'
  python run_etl.py --google

  # Executar apenas o enriquecimento e a compilação do dashboard
  python run_etl.py --enrich --compile
        """
    )
    
    parser.add_argument("--osm", action="store_true", help="Executa o crawler do OpenStreetMap (Overpass API).")
    parser.add_argument("--google", action="store_true", help="Executa o crawler do Google Places (requer chave de API).")
    parser.add_argument("--enrich", action="store_true", help="Executa o enriquecimento de dados geográficos (Nominatim).")
    parser.add_argument("--clean", action="store_true", help="Executa a normalização e limpeza dos nomes das redes operadoras no CSV.")
    parser.add_argument("--compile", action="store_true", help="Compila os dados consolidados do CSV para o JavaScript do painel.")
    parser.add_argument("--all", action="store_true", help="Executa todo o pipeline de dados de ponta a ponta na ordem correta.")
    parser.add_argument("--key", type=str, help="Chave da API Google Places (opcional, sobrescreve variável de ambiente).")
    
    args = parser.parse_args()
    
    setup_logging()
    
    # Se nenhum argumento for passado, exibe a ajuda
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)
        
    logger.info("=== Iniciando Pipeline de Processamento Eletropostos Brasil ===")
    
    try:
        # Se --all for selecionado, ativa todas as flags em sequência lógica
        if args.all:
            args.osm = True
            args.google = True
            args.clean = True
            args.enrich = True
            args.compile = True
            
        if args.osm:
            logger.info("Etapa 1: Rodando crawler do OpenStreetMap...")
            run_osm_crawler()
            
        if args.google:
            logger.info("Etapa 2: Rodando crawler do Google Places...")
            api_key = args.key or os.environ.get("GOOGLE_PLACES_API_KEY")
            if not api_key:
                logger.error("Chave do Google Places não fornecida. Etapa pulada.")
            else:
                run_google_places_crawler(api_key)
                
        if args.clean:
            logger.info("Etapa de Limpeza: Rodando normalização e limpeza das redes...")
            from config import CSV_PATH, OSM_CSV_PATH
            clean_csv(CSV_PATH)
            clean_csv(OSM_CSV_PATH)
                
        if args.enrich:
            logger.info("Etapa 3: Executando enriquecimento de dados (Nominatim)...")
            run_enrichment()
            
        if args.compile:
            logger.info("Etapa 4: Compilando dados para o Dashboard...")
            compile_csv_to_js()
            
        logger.info("=== Pipeline finalizado com sucesso! ===")
        
    except Exception as e:
        logger.error(f"Ocorreu uma falha durante a execução do pipeline: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
