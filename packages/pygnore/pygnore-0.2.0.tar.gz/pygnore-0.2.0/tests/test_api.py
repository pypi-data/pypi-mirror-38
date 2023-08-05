import os
import unittest

from pygnore.api import get_templates, get_gitignore, cache
from pygnore.exceptions import UnsupportedTemplateError

from urllib.error import URLError
from unittest.mock import patch


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.templates_list = ["python", "go", "java"]
        self.template = ["go"]
        self.file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "go.gitignoretest"
        )

    def test_templates_list(self):
        for i in self.templates_list:
            self.assertIn(i, get_templates())

    def test_gitignore_generate(self):
        generated = get_gitignore(self.template)
        with open(self.file, "r") as f:
            gitignore = f.read()
            self.assertEqual(generated, gitignore)

    def test_api_no_support(self):
        with self.assertRaises(UnsupportedTemplateError):
            get_gitignore("php")

    @patch("pygnore.api.urlopen", side_effect=URLError("No connection"))
    def test_connection_error(self, mock):
        with self.assertRaises(URLError):
            cache.clear()
            get_templates()

    @patch("pygnore.api.gitignore_api", "invalid_url/")
    def test_value_error(self):
        with self.assertRaises(ValueError):
            get_gitignore(self.templates_list)
