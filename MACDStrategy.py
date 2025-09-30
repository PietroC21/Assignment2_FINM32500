# Buy if MACD line crosses above signal line
from BenchmarkStrategy import Strategy
import pandas as pd



class MACDStrategy(Strategy):
    """
    Buy when MACD crosses ABOVE signal. Uses PriceLoader to fetch prices.
    """

    def __init__(self, symbol: str, loader: PriceLoader, fast: int = 12, slow: int = 26, signal_span: int = 9):
        super().__init__(symbol)
        if slow <= fast:
            raise ValueError("`slow` must be greater than `fast` for MACD.")
        self.fast = fast
        self.slow = slow
        self.signal_span = signal_span
        self.loader = loader

    def _macd(self, prices: pd.Series) -> pd.DataFrame:
        ema_fast = prices.ewm(span=self.fast, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal_span, adjust=False).mean()
        hist = macd_line - signal_line
        return pd.DataFrame({"MACD": macd_line, "Signal": signal_line, "Hist": hist})

    def generate_signals(self, start=None, end=None) -> pd.DataFrame:
        """
        Fetch prices via loader and produce signals & position.
        Params
        ------
        start, end : optional str/datetime-like bounds
        """
        s = self.loader.get_prices(self.symbol, start=start, end=end).astype(float)
        macd_df = self._macd(s)

        cross_up = (macd_df["MACD"].shift(1) <= macd_df["Signal"].shift(1)) & (macd_df["MACD"] > macd_df["Signal"])
        position = (macd_df["MACD"] > macd_df["Signal"]).astype(int)

        out = pd.concat([s.rename("price"), macd_df], axis=1)
        out["cross_up"] = cross_up.fillna(False)
        out["signal"] = out["cross_up"].astype(int)  # 1 only on bullish cross bars
        out["position"] = position                   # held while MACD > Signal
        return out