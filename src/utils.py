import math
import logging
import sys

def setup_logging():
    """Configura o sistema de logging para exibir informações no console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância entre duas coordenadas geográficas em metros usando a fórmula de Haversine."""
    R = 6371000  # Raio da Terra em metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def parse_address_components(formatted_address: str) -> tuple[str, str]:
    """
    Extrai heurística básica de cidade e estado (UF) de um endereço formatado do Google Maps.
    Ex: 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP, 01310-100, Brazil'
    Retorna uma tupla (cidade, estado).
    """
    if not formatted_address:
        return "", ""
        
    try:
        parts = [p.strip() for p in formatted_address.split(',')]
        if len(parts) >= 2:
            # Penúltima ou antepenúltima parte costuma ter 'Cidade - Estado'
            for part in parts:
                if ' - ' in part:
                    subparts = part.split(' - ')
                    if len(subparts) == 2 and len(subparts[1].strip()) == 2:
                        return subparts[0].strip(), subparts[1].strip().upper()
    except Exception:
        pass
    return "", ""
