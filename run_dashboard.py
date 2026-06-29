import http.server
import socketserver
import webbrowser
import os
import logging
import sys

# Adiciona o diretório src/ ao sys.path para permitir importações
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from config import ROOT_DIR, DASHBOARD_PORT
from utils import setup_logging

logger = logging.getLogger(__name__)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

def start_server(port: int = DASHBOARD_PORT):
    """Inicia o servidor de desenvolvimento para o dashboard de eletropostos."""
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"\n==============================================================")
            print(f"⚡ SERVIDOR ELETROPOSTOS BRASIL INICIADO EM: {url}")
            print(f"==============================================================")
            print("• Os dados estão sendo servidos localmente a partir de arquivos compilados.")
            print("• Alterações no CSV requerem rodar a compilação (run_etl.py --compile).")
            print("• Pressione Ctrl+C para encerrar o servidor a qualquer momento.\n")
            
            try:
                webbrowser.open(url)
            except Exception:
                logger.warning("Não foi possível abrir o navegador automaticamente.")
                
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServidor encerrado com sucesso.")
    except OSError as e:
        if e.errno == 98: # Address already in use
            logger.error(f"Erro: Porta {port} já está em uso por outro processo.")
        else:
            logger.error(f"Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    setup_logging()
    start_server()
