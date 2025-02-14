from abc import classmethod
from .base_formatter import BaseFormatter


class OpenMeteoFormatter(BaseFormatter):
    def __init__(self):
        super().__init__()

    @classmethod
    def format_data(self, data):
        pass