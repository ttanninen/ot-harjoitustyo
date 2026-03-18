import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alustetaan_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 20.00)

    def test_saldo_vahenee_jos_tarpeeksi_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)
    
    def test_saldo_ei_muutu_jos_ei_tarpeeksi_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)

    