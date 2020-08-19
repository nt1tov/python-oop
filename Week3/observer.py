from abc import ABC, abstractmethod



class ObservableEngine(Engine):  # Наблюдаемая оболочка для движений для игрового движка
    def __init__(self):
        self.__subscribers = set()
    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)
        
    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)
        
    def notify(self, achievement):
        for sub in self.__subscribers:
            sub.update(achievement)
        
    
class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass
    
class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.__name = "ShortNotificationPrinter"
        self.achievements = set()
        
    def update(self, message):
        msg_title = message['title']
        self.achievements.add(msg_title)
    
class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.__name = "FullNotificationPrinter"
        self.achievements = []
        self.__achievements = set()
        
    def update(self, message):
        msg_title = message['title']
        if msg_title not in self.__achievements:
            self.__achievements.add(msg_title)
            self.achievements.append(message)
    