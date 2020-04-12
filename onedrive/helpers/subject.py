
class Subject:

    def __init__(self):
        self.__observers = set()

    def add_observer(self, observer):
        self.__observers.add(observer)

    def notify(self):
        for observer in self.__observers:
            observer.update(self)
