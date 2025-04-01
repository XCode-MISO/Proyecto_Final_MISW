from abc import ABC, abstractmethod

class BaseCommannd(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Please implement in subclass")
