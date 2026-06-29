import unittest
import sys
import os

# Adiciona o diretório src/ ao sys.path para permitir importações
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from utils import haversine_distance, parse_address_components, normalize_network_name

class TestUtils(unittest.TestCase):
    
    def test_haversine_distance(self):
        # Coordenadas aproximadas de São Paulo e Rio de Janeiro
        sp_lat, sp_lon = -23.5615, -46.6560
        rj_lat, rj_lon = -22.9068, -43.1729
        
        # Distância aproximada real é de cerca de 360km (360000m)
        dist = haversine_distance(sp_lat, sp_lon, rj_lat, rj_lon)
        self.assertGreater(dist, 350000)
        self.assertLess(dist, 370000)
        
        # Mesmas coordenadas devem retornar distância zero
        self.assertEqual(haversine_distance(sp_lat, sp_lon, sp_lat, sp_lon), 0)

    def test_parse_address_components(self):
        # Formato padrão da API Google Places
        addr_1 = "Av. Paulista, 1000 - Bela Vista, São Paulo - SP, 01310-100, Brazil"
        cidade_1, estado_1 = parse_address_components(addr_1)
        self.assertEqual(cidade_1, "São Paulo")
        self.assertEqual(estado_1, "SP")
        
        # Formato alternativo
        addr_2 = "R. Dr. Franco da Rocha, 664 - Perdizes, São Paulo - SP, 05015-040, Brazil"
        cidade_2, estado_2 = parse_address_components(addr_2)
        self.assertEqual(cidade_2, "São Paulo")
        self.assertEqual(estado_2, "SP")
        
        # Endereço sem cidade/estado padronizados
        addr_3 = "Franco da Rocha, 664, Perdizes, Brazil"
        cidade_3, estado_3 = parse_address_components(addr_3)
        self.assertEqual(cidade_3, "")
        self.assertEqual(estado_3, "")

    def test_normalize_network_name_shell(self):
        # Shell
        self.assertEqual(normalize_network_name("Shell Recharge Solutions"), "Shell Recharge")
        self.assertEqual(normalize_network_name("Posto Shell"), "Shell Recharge")
        self.assertEqual(normalize_network_name("chell"), "Shell Recharge")
        self.assertEqual(normalize_network_name("Shell"), "Shell Recharge")

    def test_normalize_network_name_petrobras(self):
        # Petrobras
        self.assertEqual(normalize_network_name("BR"), "Petrobras")
        self.assertEqual(normalize_network_name("Petrobrás"), "Petrobras")
        self.assertEqual(normalize_network_name("Bandeira Petrobrás"), "Petrobras")
        self.assertEqual(normalize_network_name("Posto Jatobá BR"), "Petrobras")
        self.assertEqual(normalize_network_name("Petrobras Belvedere (podium)"), "Petrobras")

    def test_normalize_network_name_ipiranga(self):
        # Ipiranga
        self.assertEqual(normalize_network_name("ipiranga"), "Ipiranga")
        self.assertEqual(normalize_network_name("ipiringa"), "Ipiranga")
        self.assertEqual(normalize_network_name("Posto Ipiranga - Míriam"), "Ipiranga")

    def test_normalize_network_name_others(self):
        # Volvo, BYD, Porsche, BMW
        self.assertEqual(normalize_network_name("Volvo Car Brasil"), "Volvo")
        self.assertEqual(normalize_network_name("Maggi BYD"), "BYD")
        self.assertEqual(normalize_network_name("BMW"), "BMW")
        self.assertEqual(normalize_network_name("Porsche Charger"), "Porsche")
        self.assertEqual(normalize_network_name("EDP Smart"), "EDP")
        self.assertEqual(normalize_network_name("Enel X Way"), "Enel X")

    def test_normalize_network_name_independente(self):
        # Estabelecimentos que viram Independente
        self.assertEqual(normalize_network_name("Padaria Real"), "Independente")
        self.assertEqual(normalize_network_name("Auto Posto Pomerode"), "Independente")
        self.assertEqual(normalize_network_name("Hotel Universitário"), "Independente")
        self.assertEqual(normalize_network_name("Restaurante Wunderwald"), "Independente")
        self.assertEqual(normalize_network_name("Tipo 1 (SAE J1772)"), "Independente")
        self.assertEqual(normalize_network_name("automático"), "Independente")
        self.assertEqual(normalize_network_name("1"), "Independente")

    def test_normalize_network_name_preserve_unmapped(self):
        # Redes legítimas não mapeadas devem preservar a capitalização limpa
        self.assertEqual(normalize_network_name("EzVolt"), "EzVolt")
        self.assertEqual(normalize_network_name("Eletra"), "Eletra")

if __name__ == "__main__":
    unittest.main()
