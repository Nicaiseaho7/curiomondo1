#!/usr/bin/env python3
import json, re, unittest
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ConcertTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=json.loads((ROOT/'assets/data/concerti.json').read_text(encoding='utf-8'))
    def test_required_files(self):
        for path in ('concerti/index.html','concerti/archivio/index.html','assets/css/concerti-v1.css','assets/js/concerti-v1.js','assets/images/concerti/concerti-italia-hero-480.webp','assets/images/concerti/concerti-italia-hero-800.webp','assets/images/concerti/concerti-italia-hero-1200.webp'): self.assertTrue((ROOT/path).is_file(),path)
    def test_unique_ids_and_valid_dates(self):
        ids=[e['id'] for e in self.data['events']]; self.assertEqual(len(ids),len(set(ids)))
        for event in self.data['events']: datetime.fromisoformat(event['start']); datetime.fromisoformat(event['lastVerified'])
    def test_sources_and_regions(self):
        allowed={'Abruzzo','Basilicata','Calabria','Campania','Emilia-Romagna','Friuli-Venezia Giulia','Lazio','Liguria','Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino-Alto Adige','Umbria','Valle d’Aosta','Veneto'}
        for event in self.data['events']:
            self.assertIn(event['region'],allowed); self.assertRegex(event['sourceUrl'],r'^https://'); ticket=event.get('ticketUrl') or ''
            if ticket: self.assertRegex(ticket,r'^https://')
    def test_no_duplicate_artist_city_datetime(self):
        keys=[(e['artist'].casefold(),e['city'].casefold(),e['start']) for e in self.data['events']]; self.assertEqual(len(keys),len(set(keys)))
    def test_page_contract(self):
        html=(ROOT/'concerti/index.html').read_text(encoding='utf-8'); self.assertIn('id="concertFilters"',html); self.assertIn('/concerti/archivio/',html); self.assertIn('aria-live="polite"',html); self.assertNotIn('aggiornamento automatico',html.lower())
if __name__=='__main__': unittest.main(verbosity=2)
