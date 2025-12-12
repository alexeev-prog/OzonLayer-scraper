from enum import Enum
from pathlib import Path

import orjson as json
import toml
import yaml


class ConfigType(Enum):
    TOML = 0
    YAML = 1
    JSON = 2


def detect_config_type_by_extension(extension: str) -> ConfigType:
    cleaned_extension = extension.lower().lstrip(".")

    if cleaned_extension == "json":
        return ConfigType.JSON
    if cleaned_extension in ("yaml", "yml"):
        return ConfigType.YAML
    if cleaned_extension == "toml":
        return ConfigType.TOML
    return ConfigType.JSON


def detect_config_type_by_filename(filename: str) -> ConfigType:
    extension = Path(filename).suffix.lstrip(".") or filename
    return detect_config_type_by_extension(extension)


class ConfigReader:
    def __init__(self, config_file: str, configtype: ConfigType = None):
        self.config_file = Path(config_file)

        if configtype is None:
            self.configtype = detect_config_type_by_filename(config_file)
        else:
            self.configtype = configtype

        self.config = self._load_data_from_config()

    def _load_data_from_config(self) -> dict:
        data = {}

        if not self.config_file.exists():
            return data

        if self.configtype == ConfigType.YAML:
            with self.config_file.open() as f:
                data = yaml.safe_load(f)
        elif self.configtype == ConfigType.TOML:
            with self.config_file.open() as f:
                data = toml.load(f)
        elif self.configtype == ConfigType.JSON:
            with self.config_file.open("rb") as f:
                data = json.loads(f.read())

        return data if isinstance(data, dict) else {}
