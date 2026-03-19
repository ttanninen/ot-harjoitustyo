import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_aloitussaldo_ilman_myyntia_on_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_toimii(self):
        self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),(100000 + 240) / 100)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kateisella_toimii(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),(100000 + 400) / 100)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_edullisesti_kateisella_ei_tarpeeksi_rahaa(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_syo_maukkaasti_kateisella_ei_tarpeeksi_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kortilla_toimii(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_syo_maukkaasti_kortilla_toimii(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_syo_edullisesti_kortilla_ei_tarpeeksi_rahaa(self):
        maksukortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(maksukortti.saldo, 200)

    def test_syo_maukkaasti_kortilla_ei_tarpeeksi_rahaa(self):
        maksukortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(maksukortti.saldo, 200)

    def test_rahan_lataus_kortille_toimii(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100200)
        self.assertEqual(self.maksukortti.saldo, 1200)

    def test_lataa_negatiivinen_summa_kortille(self):
        self.assertEqual(self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -200), None)