#!/usr/bin/env python3
import json,re,unittest
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads((ROOT/'assets/data/scadenze.json').read_text(encoding='utf-8'))
    def test_ids_slugs_unique(self):
        for key in ('id','slug'):
            values=[x[key] for x in self.data['items']];self.assertEqual(len(values),len(set(values)))
    def test_dates_sources(self):
        for item in self.data['items']:
            datetime.fromisoformat(item['date']);datetime.fromisoformat(item['lastVerified']);self.assertRegex(item['sourceUrl'],r'^https://');self.assertIn(item['dateType'],{'scadenza','apertura'})
    def test_static_pages(self):
        for item in self.data['items']:
            page=ROOT/'scadenze'/item['slug']/'index.html';self.assertTrue(page.is_file(),page);text=page.read_text(encoding='utf-8');self.assertIn('<meta name="robots" content="index,follow',text);self.assertIn('<link rel="canonical"',text);self.assertIn('application/ld+json',text);self.assertIn(item['title'],text)
    def test_index_contract(self):
        text=(ROOT/'scadenze/index.html').read_text(encoding='utf-8');self.assertIn('id="deadlineFilters"',text);self.assertIn('id="deadlineGroups"',text);self.assertIn('DEADLINE_STATIC_DIRECTORY_START',text);self.assertNotIn('aggiornamento automatico',text.lower())
    def test_sitemap_complete(self):
        text=(ROOT/'sitemap-scadenze.xml').read_text(encoding='utf-8');self.assertEqual(text.count('<url>'),len(self.data['items'])+2)
        for item in self.data['items']:self.assertIn(f'/scadenze/{item["slug"]}/',text)
    def test_no_duplicate_title_date(self):
        keys=[(x['title'].casefold(),x['date']) for x in self.data['items']];self.assertEqual(len(keys),len(set(keys)))
if __name__=='__main__':unittest.main(verbosity=2)
