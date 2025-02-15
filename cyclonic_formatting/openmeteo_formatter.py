from .base_formatter import BaseFormatter

class OpenMeteoFormatter(BaseFormatter):
    def __init__(self):
        super().__init__()

    def format_data(self, response):
        return {
            "lat": response.Latitude(),
            "long": response.Longitude(),
            "elevation": response.Elevation(), # m asl
            "timezone": response.Timezone()
        }