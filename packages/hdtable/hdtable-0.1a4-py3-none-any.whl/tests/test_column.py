import os
import unittest

import yaml

from hdtable.hdtable import Column


class TestColumn(unittest.TestCase):
    def setUp(self) -> None:
        current_dirpath = os.path.dirname(os.path.abspath(__file__))
        specs_filepath = os.path.join(current_dirpath, "specs", "sample.yml")

        with open(specs_filepath, "r") as f:
            self.specs = yaml.safe_load(f)

    def test_attributes(self) -> None:
        for i, spec in enumerate(self.specs):
            c = Column(i, spec)

            self.assertEqual(c.index, i)
