""" Test parsing a variety of hcl files"""
import json
import os
from unittest import TestCase

from sculpt import hcl

HCL_DIR = "terraform-config"
JSON_DIR = "terraform-config-json"


class TestLoad(TestCase):
    """Test parsing a variety of hcl files"""

    def setUp(self):
        self.prev_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(__file__), "../helpers"))

    def test_load_terraform(self):
        """Test parsing a set of hcl files from a cached parser file"""
        self._load_test_files()

    def _load_test_files(self):
        """Recursively parse all files in a directory"""
        # pylint: disable=unused-variable
        for current_dir, _dirs, files in os.walk("terraform-config"):
            dir_prefix = os.path.commonpath([HCL_DIR, current_dir])
            relative_current_dir = current_dir.replace(dir_prefix, "")
            current_out_dir = os.path.join(JSON_DIR, relative_current_dir)
            for file_name in files:
                # file_name = "backend.tf"
                file_path = os.path.join(current_dir, file_name)
                json_file_path = os.path.join(current_out_dir, file_name)
                json_file_path = os.path.splitext(json_file_path)[0] + ".json"

                with self.subTest(msg=file_path):
                    if file_name.startswith("bad_"):
                        with open(file_path, encoding="utf8") as hcl_file:
                            try:
                                hcl.load(hcl_file)
                                self.fail("Should throw parsing error for file")
                            except Exception as err:
                                if not str(err).startswith("Line has unclosed quote marks"):
                                    self.fail(f"Got an unexpected error, {err}")
                    else:
                        with open(file_path, encoding="utf8") as hcl_file, open(
                            json_file_path,
                            encoding="utf8",
                        ) as json_file:
                            hcl_dict = hcl.load(hcl_file)
                            json_dict = json.load(json_file)

                            self.assertDictEqual(hcl_dict, json_dict, msg=f"missmatch found in {file_name}")
                # break
