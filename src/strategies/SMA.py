
from strategies.strategy import Strategy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class SMA(Strategy):
    '''
    Simple Moving Average (SMA) trading strategy.
    '''

    def __init__(self, short_window: int = 50, long_window: int = 200) -> None:
        super().__init__()

        self.short_window = short_window
        self.long_window = long_window

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        '''
        Execute the SMA trading strategy on the provided data.

        Args:
            data (pd.DataFrame): DataFrame containing historical price data.
        
        Returns:
            pd.DataFrame: DataFrame with trading signals.
        '''

        # Calculate short and long SMAs
        data['short_sma'] = data['Close'].rolling(window=self.short_window).mean()
        data['long_sma'] = data['Close'].rolling(window=self.long_window).mean()

        # Generate trading signals
        signals = np.zeros(len(data))
        signals[data['short_sma'] > data['long_sma']] = 1
        signals[data['short_sma'] < data['long_sma']] = -1

        prev_signals = np.zeros(len(data))
        prev_signals[1:] = signals[:-1]  # Shift signals to compare with

        signals[signals == prev_signals] = 0  # No change in signal
        data['signal'] = signals

        self.data = data
        return data


    def plot_signals(self) -> None:
        fig, ax = super().plot_signals()

        ax.plot(self.data['short_sma'], label=f'Short SMA ({self.short_window})', color='cornflowerblue', linewidth=2)
        ax.plot(self.data['long_sma'], label=f'Long SMA ({self.long_window})', color='mediumseagreen', linewidth=2)

        ax.set_title('SMA Strategy Signals')
        ax.legend()

        plt.show()