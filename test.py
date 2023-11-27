import unittest
import requests

class DatamartTests(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'

    def test_datamart_active(self):
        URL = f'{self.base_url}/download/RUC/20601099251'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 200)

    def test_datamart_inactive(self):
        URL = f'{self.base_url}/download/RUC/0'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 400)
