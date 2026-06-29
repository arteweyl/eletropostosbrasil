import os
import sys

# Adiciona o diretório src/ ao sys.path para permitir importações
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from utils import haversine_distance, parse_address_components, normalize_network_name

def test_haversine_distance():
    """Valida a precisão dos cálculos de distâncias geográficas usando Haversine."""
    # Coordenadas aproximadas de São Paulo e Rio de Janeiro
    sp_lat, sp_lon = -23.5615, -46.6560
    rj_lat, rj_lon = -22.9068, -43.1729
    
    dist = haversine_distance(sp_lat, sp_lon, rj_lat, rj_lon)
    assert 350000 < dist < 370000
    assert haversine_distance(sp_lat, sp_lon, sp_lat, sp_lon) == 0

def test_parse_address_components():
    """Valida a extração de cidade e estado a partir do endereço formatado."""
    # Formato padrão da API Google Places
    addr_1 = "Av. Paulista, 1000 - Bela Vista, São Paulo - SP, 01310-100, Brazil"
    cidade_1, estado_1 = parse_address_components(addr_1)
    assert cidade_1 == "São Paulo"
    assert estado_1 == "SP"
    
    # Formato alternativo
    addr_2 = "R. Dr. Franco da Rocha, 664 - Perdizes, São Paulo - SP, 05015-040, Brazil"
    cidade_2, estado_2 = parse_address_components(addr_2)
    assert cidade_2 == "São Paulo"
    assert estado_2 == "SP"
    
    # Endereço sem cidade/estado padronizados
    addr_3 = "Franco da Rocha, 664, Perdizes, Brazil"
    cidade_3, estado_3 = parse_address_components(addr_3)
    assert cidade_3 == ""
    assert estado_3 == ""

def test_normalize_network_name_shell():
    """Valida a normalização de diferentes grafias para a rede Shell Recharge."""
    assert normalize_network_name("Shell Recharge Solutions") == "Shell Recharge"
    assert normalize_network_name("Posto Shell") == "Shell Recharge"
    assert normalize_network_name("chell") == "Shell Recharge"
    assert normalize_network_name("Shell") == "Shell Recharge"

def test_normalize_network_name_petrobras():
    """Valida a normalização de diferentes grafias para a rede Petrobras."""
    assert normalize_network_name("BR") == "Petrobras"
    assert normalize_network_name("Petrobrás") == "Petrobras"
    assert normalize_network_name("Bandeira Petrobrás") == "Petrobras"
    assert normalize_network_name("Posto Jatobá BR") == "Petrobras"
    assert normalize_network_name("Petrobras Belvedere (podium)") == "Petrobras"

def test_normalize_network_name_ipiranga():
    """Valida a normalização de diferentes grafias para a rede Ipiranga."""
    assert normalize_network_name("ipiranga") == "Ipiranga"
    assert normalize_network_name("ipiringa") == "Ipiranga"
    assert normalize_network_name("Posto Ipiranga - Míriam") == "Ipiranga"

def test_normalize_network_name_others():
    """Valida a normalização de outras redes operadoras mapeadas."""
    assert normalize_network_name("Volvo Car Brasil") == "Volvo"
    assert normalize_network_name("Maggi BYD") == "BYD"
    assert normalize_network_name("BMW") == "BMW"
    assert normalize_network_name("Porsche Charger") == "Porsche"
    assert normalize_network_name("EDP Smart") == "EDP"
    assert normalize_network_name("Enel X Way") == "Enel X"

def test_normalize_network_name_independente():
    """Valida que postos locais genéricos ou conectores são remapeados para Independente."""
    assert normalize_network_name("Padaria Real") == "Independente"
    assert normalize_network_name("Auto Posto Pomerode") == "Independente"
    assert normalize_network_name("Hotel Universitário") == "Independente"
    assert normalize_network_name("Restaurante Wunderwald") == "Independente"
    assert normalize_network_name("Tipo 1 (SAE J1772)") == "Independente"
    assert normalize_network_name("automático") == "Independente"
    assert normalize_network_name("1") == "Independente"

def test_normalize_network_name_preserve_unmapped():
    """Valida que marcas e operadoras legítimas não mapeadas são preservadas."""
    assert normalize_network_name("EzVolt") == "EzVolt"
    assert normalize_network_name("Eletra") == "Eletra"
