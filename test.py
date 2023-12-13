import unittest
import requests

class DatamartTests(unittest.TestCase):
    base_url = 'http://twh.factura-negociable.net.pe:7074'

    # ------------------- TESTS DE RUC -------------------
    def test_ruc_datamart_active(self):
        URL = f'{self.base_url}/download/RUC/20506151547'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 200)

        if r.status_code == 200:
            # Verificar mensaje de respuesta (JSON)
            self.assertEqual(r.json()['code'], '200')
            self.assertEqual(r.json()['message'], 'Documento descargado')

    def test_ruc_datamart_inactive(self):
        URL = f'{self.base_url}/download/RUC/0'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 400)

        if r.status_code == 400:
            # Verificar mensaje de respuesta (JSON)
            self.assertEqual(r.json()['code'], '301')
            self.assertEqual(r.json()['message'], 'Subscripcion inactiva')

    # ------------------- TESTS DE RTT -------------------
    def test_rtt_datamart_active(self):
        URL = f'{self.base_url}/download/RTT/20506151547'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 200)

        if r.status_code == 200:
            # Verificar mensaje de respuesta (JSON)
            self.assertEqual(r.json()['code'], '200')
            self.assertEqual(r.json()['message'], 'Documento descargado')

    def test_rtt_datamart_inactive(self):
        URL = f'{self.base_url}/download/RTT/0'

        # Enviar solicitud
        r = requests.get(URL)

        # Verificar respuesta
        self.assertEqual(r.status_code, 400)

        if r.status_code == 400:
            # Verificar mensaje de respuesta (JSON)
            self.assertEqual(r.json()['code'], '301')
            self.assertEqual(r.json()['message'], 'Subscripcion inactiva')

if __name__ == '__main__':
    unittest.main()
