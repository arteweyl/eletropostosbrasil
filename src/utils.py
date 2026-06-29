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

def normalize_network_name(raw_name: str, station_name: str = "") -> str:
    """
    Normaliza o nome da rede operadora com base em regras e heurísticas de palavras-chave.
    """
    if not raw_name:
        raw_name = ""
    if not station_name:
        station_name = ""
        
    name_to_check = f"{raw_name} {station_name}".lower()
    
    # Heurísticas de correspondência de palavras-chave (Redes Específicas primeiro)
    if "tupinambá" in name_to_check or "tupinamba" in name_to_check:
        return "Tupinambá"
    if "shell" in name_to_check or "chell" in name_to_check:
        return "Shell Recharge"
    if "raízen" in name_to_check or "raizen" in name_to_check:
        return "Raízen Power"
    if "volvo" in name_to_check:
        return "Volvo"
    if "byd" in name_to_check:
        return "BYD"
    if "ipiranga" in name_to_check or "ipiringa" in name_to_check:
        return "Ipiranga"
    if "weg" in name_to_check:
        return "WEG"
    if "porsche" in name_to_check:
        return "Porsche"
    if "bmw" in name_to_check:
        return "BMW"
    if "edp" in name_to_check:
        return "EDP"
    if "zletric" in name_to_check:
        return "Zletric"
    if "neoenergia" in name_to_check:
        return "Neoenergia"
    if "enel" in name_to_check:
        return "Enel X"
    if "copel" in name_to_check:
        return "Copel"
    if "cpfl" in name_to_check:
        return "CPFL"
    if "taurus" in name_to_check:
        return "Taurus"
    if "gwm" in name_to_check:
        return "GWM"
    if "incharge" in name_to_check:
        return "Incharge"
    if "go electric" in name_to_check or "go eletric" in name_to_check:
        return "Go Electric"
    if "eletrograal" in name_to_check:
        return "Eletrograal"
    if "abb" in name_to_check:
        return "ABB"
    if "audi" in name_to_check:
        return "Audi"
    if "renault" in name_to_check:
        return "Renault"
    if "chargepoint" in name_to_check:
        return "ChargePoint"
    if "chargeon" in name_to_check:
        return "ChargeOn"
    if "fastev" in name_to_check:
        return "FastEV"
    if "planeta charge" in name_to_check:
        return "Planeta Charge"
    if "joy energy" in name_to_check:
        return "Joy Energy"
    if "ecocarga" in name_to_check:
        return "EcoCarga"

    # Tokenização inteligente para marcas genéricas/ambíguas como "BR" (Petrobras)
    clean_text = name_to_check.replace("(", " ").replace(")", " ").replace("/", " ").replace("-", " ").replace(",", " ")
    words = clean_text.split()
    
    if "petrobras" in words or "petrobrás" in words or "br" in words or "petrox" in words or "petrobras" in name_to_check or "petrobrás" in name_to_check:
        return "Petrobras"
        
    # Limpezas genéricas
    raw_cleaned = raw_name.strip()
    if raw_cleaned in ["1", "automático", "tipo 1 (sae j1772)", "Bandeira Branca", "Bandeira branca", "BANDEIRA BRANCA", "Tipo 1 (SAE J1772)"]:
        return "Independente"
        
    raw_lower = raw_cleaned.lower()
    if any(k in raw_lower for k in ["auto posto", "posto ", "restaurante", "hotel", "balsa", "padaria", "hospital", "shopping", "patio", "parceria", "escola", "clube"]):
        return "Independente"
        
    # Se for uma rede/empresa legítima de tamanho pequeno ou não mapeada, preservamos a capitalização limpa
    if raw_cleaned and raw_cleaned != "None":
        return raw_cleaned
        
    return "Independente"
