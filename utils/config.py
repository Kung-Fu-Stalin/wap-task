from pathlib import Path
from typing import Union
from dataclasses import dataclass

import yaml


@dataclass
class Device:
    name: str
    height: int
    width: int


class Config:
    PROJECT_PATH = Path(__file__).resolve().parent.parent
    CONFIG_PATH = Path(PROJECT_PATH, "config", "config.yml")
    SCREENSHOTS_PATH = Path(PROJECT_PATH, "screenshots")
    SCREENSHOTS_PATH.mkdir(parents=True, exist_ok=True)

    def __init__(self) -> None:
        self.data = self.read_data(self.CONFIG_PATH)
        self._validate_attributes()
        self._set_device_attributes()
        self._set_config_attributes()

    @staticmethod
    def read_data(config_path: Union[str, Path]) -> dict:
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _set_device_attributes(self) -> None:
        test_device = self.data["device"]
        for device in self.data["devices"]:
            if device.get(test_device):
                device = Device(
                    name=test_device,
                    height=device[test_device]["height"],
                    width=device[test_device]["width"]
                )
                setattr(self, "DEVICE", device)
        self.data.pop("devices")
        self.data.pop("device")

    def _set_config_attributes(self) -> None:
        for key, value in self.data.items():
            setattr(self, key.upper(), value.lower())

    def _validate_attributes(self) -> None:
        devices = [list(d.keys())[0] for d in self.data["devices"]]
        browsers = ["chrome", "firefox"]

        t_browser = self.data.get("browser").lower()
        t_device = self.data.get("device").lower()

        if t_browser not in browsers:
            raise ValueError(
                f"Incorrect testing browser: {t_browser}. "
                f"Correct browsers: {browsers}"
            )
        if t_device not in devices:
            raise ValueError(
                f"Incorrect testing device: {t_device}. "
                f"Correct devices: {devices}"
            )

Config = Config()
