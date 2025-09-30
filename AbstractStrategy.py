from abc import abstractmethod, ABC
import pandas as pd
from PriceLoader import PriceLoader

class Strategy(ABC):       
    @abstractmethod
    def generate_signals(self, tick) -> pd.DataFrame:
        pass
