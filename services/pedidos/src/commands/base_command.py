#./commands/base_command.py
from abc import ABC, abstractmethod

class BaseCommannd(ABC):
    @abstractmethod
    def execute(self): # pragma: no cover
        raise NotImplementedError("Please implement in subclass")