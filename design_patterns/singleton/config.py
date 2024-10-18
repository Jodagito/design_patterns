import json
import os

from dotenv import load_dotenv

from design_patterns.dataclasses.config import Config


class ConfigsLoader:
    _instance = None
    _config: Config = None
    _absolute_configs_file_path = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigsLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        self._set_absolute_configs_file_path()

    def load_configs(self) -> None:
        with open(self._absolute_configs_file_path) as configs_file:
            configs_file_content = json.load(configs_file)
        self._set_configs(configs_file_content)

    def get_configs(self) -> Config:
        if self._config is None:
            raise ValueError("Configs have not been loaded yet")
        return self._config

    def _set_absolute_configs_file_path(self) -> None:
        run_mode = os.getenv('RUN_MODE')
        _relative_configs_file_path = f"config\\{run_mode}\\configs.json"
        if self._absolute_configs_file_path is None:
            self._absolute_configs_file_path = os.path.join(
                os.getcwd(), _relative_configs_file_path)

    def _set_configs(self, configs_file_content: dict) -> None:
        self._config = Config(**configs_file_content)
