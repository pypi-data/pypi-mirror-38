import os

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin

from pygnore.exceptions import NoSupportedTemplate
from cachetools import cached, TTLCache

GITIGNORE_SERVER = os.environ.get("GITIGNORE_SERVER", "https://gitignore.io/api/")

gitignore_api = (
    GITIGNORE_SERVER if GITIGNORE_SERVER.endswith("/") else GITIGNORE_SERVER + "/"
)


cache = TTLCache(maxsize=1, ttl=300)


@cached(cache)
def get_templates():
    request = urljoin(gitignore_api, "list")

    try:
        response = urlopen(request).read().decode()
    except (HTTPError, URLError, ValueError):
        raise

    pre_formated_list = [i for i in response.split("\n")]

    templates_list = []

    for i in pre_formated_list:
        templates_list.extend(i.split(","))

    return templates_list


def get_gitignore(templates):
    templates_list = get_templates()

    for i in templates:
        if i.lower() not in templates_list:
            raise NoSupportedTemplate(i)

    formated_templates = ",".join(templates)

    request = urljoin(gitignore_api, formated_templates)
    try:
        response = urlopen(request).read().decode()
    except (HTTPError, URLError, ValueError):
        raise

    return response.strip()
