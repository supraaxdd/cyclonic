from abc import abstractmethod

class BaseRequester:
    def __init__(self):
        pass

    @abstractmethod
    def prepare_request(self, **kwargs):
        pass

    @abstractmethod
    def send_request(self, params):
        pass