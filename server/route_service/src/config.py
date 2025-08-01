import os
from abc import ABC
from dataclasses import asdict, dataclass


class CfgBase(ABC):
    dict: callable = asdict

class PostgresCfg(CfgBase):
    url: str = os.getenv("DATABASE_URL")