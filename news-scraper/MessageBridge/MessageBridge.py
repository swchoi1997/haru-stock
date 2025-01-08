from abc import abstractmethod, ABC


class MessageConsumer(ABC):
    @abstractmethod
    def consume(self, is_running):
        pass


class MessageProducer(ABC):
    @abstractmethod
    def produce(self, is_running):
        pass
