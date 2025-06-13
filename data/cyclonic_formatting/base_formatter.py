from abc import abstractmethod

class BaseFormatter:
    def __init__(self):
        pass

    @abstractmethod
    def format_data(self, data):
        pass

    @abstractmethod
    def write(self, data):
        pass