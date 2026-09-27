import unittest
from lxml import html
from tools.editorial_rules import format_errors, source_errors


class EditorialRulesTest(unittest.TestCase):
    def body(self, fmt, words):
        return html.fromstring(f'<article data-article-format="{fmt}"><p>{"fatto " * words}</p></article>')

    def test_short_flash_has_no_artificial_minimum(self):
        self.assertEqual(format_errors(self.body('flash', 78)), [])

    def test_empty_article_is_blocked(self):
        self.assertIn('corpo articolo vuoto', format_errors(self.body('flash', 0)))

    def test_v4_must_declare_its_format(self):
        body = self.body('standard', 350)
        body.set('data-editorial-protocol', '4.0')
        del body.attrib['data-article-format']
        self.assertIn('formato editoriale non valido', format_errors(body))

    def test_format_boundary_does_not_leave_251_to_299_word_gap(self):
        self.assertEqual(format_errors(self.body('flash', 299)), [])
        self.assertTrue(format_errors(self.body('flash', 300)))
        self.assertTrue(format_errors(self.body('standard', 299)))
        self.assertEqual(format_errors(self.body('standard', 650)), [])

    def test_internal_method_link_is_not_independent_confirmation(self):
        doc = html.fromstring('<div><article data-risk-level="A"/><div class="art-sources"><a href="https://source.example/story">Fonte</a><a href="/pagine/metodo-editoriale.html">Metodo</a></div></div>')
        self.assertTrue(source_errors(doc, doc.xpath('//article')[0]))
        doc.xpath('//article')[0].set('data-risk-level', 'B')
        self.assertEqual(source_errors(doc, doc.xpath('//article')[0]), [])


if __name__ == '__main__':
    unittest.main()
