import os
import shutil
import tempfile

from unittest import TestCase
from unittest.mock import patch

from pygnore.exceptions import UnsupportedTemplateError
from pygnore.gitignore import Gitignore


class TestGitignore(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.template_list = ["python", "go", "java", "c++"]
        cls.dir = os.path.dirname(os.path.realpath(__file__))
        cls.file = os.path.join(cls.dir, "python.gitignoretest")

    def test_read_gitignore_current(self):
        gitignore = Gitignore(self.template_list, self.file)
        self.assertListEqual(gitignore.read(True).stack, ["python"])

    def test_read_gitignore_add(self):
        gitignore = Gitignore(self.template_list, self.file)
        self.assertListEqual(gitignore.read().stack, ["c++", "go", "java"])

    def test_read_gitignore_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Gitignore(self.template_list, "/something/not/founded")

    @patch("pygnore.gitignore.open", side_effect=PermissionError)
    def test_read_gitignore_no_permission(self, mock):
        with self.assertRaises(PermissionError):
            gitignore = Gitignore(self.template_list, self.file)
            gitignore.read(True)

    def test_gitignore_generate(self):
        gitignore = Gitignore(["python"])
        generated = gitignore.generate()
        with open(self.file, "r") as f:
            gitignore = f.read()
            self.assertEqual(generated, gitignore)

    def test_gitignore_write(self):
        gitignore = Gitignore(["python"], self.temp_dir)
        written = gitignore.generate(True, mode="w")
        with open(self.file, "r") as f:
            written_file = f.read()
            self.assertEqual(written.strip(), written_file)

    def test_template_search(self):
        gitignore = Gitignore(["pyth"])
        result = gitignore.template_search()
        self.assertEqual(result, ["python"])

    def test_generate_no_support(self):
        with self.assertRaises(UnsupportedTemplateError):
            gitignore = Gitignore(["php"])
            gitignore.generate()

    def test_generate_value_error(self):
        with self.assertRaises(ValueError):
            gitignore = Gitignore()
            gitignore.generate()

    def test_read_value_error(self):
        with self.assertRaises(ValueError):
            gitignore = Gitignore()
            gitignore.read()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
