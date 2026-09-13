import unittest
import base64
from scripts.security_scan import inspect_text

class SecretDetection(unittest.TestCase):
    def test_masked_provider_keys_are_rejected(self):
        findings,_,_=inspect_text('sk'+'-abc...xyz','fixture.txt')
        self.assertTrue(findings)
    def test_base64_credential_assignment_is_rejected(self):
        encoded=base64.b64encode(b'Nonsecret fixture data for scanner').decode('ascii')
        value='api_key'+' = '+chr(34)+encoded+chr(34)
        self.assertTrue(inspect_text(value,'fixture.txt')[0])
    def test_hex_secret_is_not_excused_as_digest(self):
        value='api_key'+' = '+chr(34)+'0123456789abcdef'*4+chr(34)
        self.assertTrue(inspect_text(value,'fixture.txt')[0])
        short='password'+' = '+chr(34)+'abc'+str(123)+chr(34)
        self.assertTrue(inspect_text(short,'fixture.txt')[0])
    def test_blank_and_required_placeholder(self):
        for value in ('','YOUR_API_KEY','your_key_here','<YOUR_API_KEY>'):
            self.assertFalse(inspect_text('TAVILY_API_KEY'+'='+value,'fixture.env')[0])
