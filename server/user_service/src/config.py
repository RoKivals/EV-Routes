import os
from abc import ABC
from dataclasses import asdict, dataclass
import logging


class CfgBase(ABC):
    dict: callable = asdict

class PostgresCfg(CfgBase):
    url: str = os.getenv("DATABASE_URL")

class ServiceLogger():
    def __init__(self):
        self.baseconfig = logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("service.log")
            ]
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self):
        return self.logger