from urllib.parse import urlparse

TRUSTED_SOURCES = [
    # International
    "bbc.com",
    "reuters.com",
    "theguardian.com",
    "nytimes.com",
    "who.int",
    "nature.com",

    # Indian trusted media
    "timesofindia.indiatimes.com",
    "thehindu.com",
    "hindustantimes.com"
]

def check_source(url):
    domain = urlparse(url).netloc.replace("www.", "")
    if domain in TRUSTED_SOURCES:
        return "KNOWN / TRUSTED", domain
    return "UNVERIFIED", domain
