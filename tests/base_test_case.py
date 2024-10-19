from unittest import TestCase

from design_patterns.singleton.config import ConfigsLoader


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        ConfigsLoader().load_configs()
