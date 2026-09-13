"""Validate citation links before either HTML or Markdown output; no fetching."""
import re
from urllib.parse import urlsplit, quote, urlunsplit

def safe_url(value):
    if not isinstance(value,str) or re.search(r'[\x00-\x20\x7f\\]',value):
        return ''
    try:
        parsed=urlsplit(value)
        if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username is not None or parsed.password is not None:
            return ''
        parsed.port
    except ValueError:
        return ''
    # Delimiters are encoded so external text cannot terminate a Markdown link.
    return urlunsplit((parsed.scheme,parsed.netloc,quote(parsed.path,safe='/%:@-._~!$&*+,;='),quote(parsed.query,safe='/%?:@-._~!$&*+,;='),quote(parsed.fragment,safe='/%?:@-._~!$&*+,;=')))
