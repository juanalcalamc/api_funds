# def send_notification(method: str, message: str):
#     if method == "email":
#         print(f" Email sent: {message}")
#     elif method == "sms":
#         print(f" SMS sent: {message}")
#     else:
#         print(f" Unknown notification method: {method}")

from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class Email(NotificationStrategy):
    def send(self, message: str):
        print(f" Email sent: {message}")

class SMS(NotificationStrategy):
    def send(self, message:str):
        print(f" SMS sent: {message}")

class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def send_notification(self, message: str):
        self._strategy.send(message)