import unittest
from portfolio_code.safe_url import safe_url

class CitationSecurity(unittest.TestCase):
    def test_dangerous_protocols(self):
        for url in ('javascript:alert(1)','data:text/html,payload','file:///example','//example.org','https://example.org/\npath'):
            with self.subTest(url=url):self.assertEqual(safe_url(url),'')
    def test_userinfo_and_invalid_ports(self):
        for url in ('https://example@example.org/','https://example.org:invalid/','https://[invalid/'):
            self.assertEqual(safe_url(url),'')
    def test_markdown_delimiters(self):
        self.assertNotIn(')',safe_url('https://example.org/a(b)'))
        self.assertEqual(safe_url('https://example.org/path?q=sample'),'https://example.org/path?q=sample')

