import os
from unittest.mock import patch

from design_patterns.singleton.config import ConfigsLoader

from tests.base_test_case import BaseTestCase


class TestConfig(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        ConfigsLoader._instance = None

    def test_is_singleton(self):
        first_instance = ConfigsLoader()
        second_instance = ConfigsLoader()
        assert isinstance(first_instance, ConfigsLoader)
        assert first_instance == second_instance

    def test_load_configs(self):
        configs_loader = ConfigsLoader()
        configs_loader.load_configs()
        assert configs_loader.get_configs()

    def test_get_configs_not_loaded(self):
        configs_loader = ConfigsLoader()
        with self.assertRaises(ValueError) as ctxt:
            configs_loader.get_configs()
            assert ctxt.msg == "Configs have not been loaded yet"

    @patch.dict(os.environ, {'RUN_MODE': 'test'})
    def test_run_mode_test_env_var(self):
        configs_loader = ConfigsLoader()
        configs_loader.load_configs()
        configs = configs_loader.get_configs()
        assert configs.sinch_api_token == "test_value"

    @patch.dict(os.environ, {'RUN_MODE': 'prod'})
    def test_run_mode_prod_env_var(self):
        configs_loader = ConfigsLoader()
        configs_loader.load_configs()
        configs = configs_loader.get_configs()
        assert configs.sinch_api_token == "prod_value"
