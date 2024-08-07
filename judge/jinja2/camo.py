from judge.jinja2 import registry
from judge.utils.camo import client as camo_client


@registry.filter
def camo(url):
    if camo_client is None:
        return url
    return camo_client.rewrite_url(url)
