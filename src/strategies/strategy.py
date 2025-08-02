import matplotlib.pyplot as plt


class Strategy:
    '''
    Base class for trading strategies.
    '''

    def __init__(self):
        self.data = None

    def execute(self, data):
        '''
        Execute the trading strategy on the provided data.

        Args:
            data (pd.DataFrame): DataFrame containing historical price data.
        
        Returns:
            pd.DataFrame: DataFrame with trading signals.
        '''
        pass

    def pnl(self, initial_cash: float = 1000000) -> float:
        '''
        Calculate the profit and loss of the strategy.

        Args:
            initial_cash (float): Initial cash available for trading.

        Returns:
            float: Final portfolio value after executing the strategy.
        '''
        
        cash = initial_cash
        shares = 0

        for _, row in self.data.iterrows():
            if row['signal'] == 1:  # Buy signal
                shares_to_buy = cash // row['Close']

                shares += shares_to_buy
                cash -= shares_to_buy * row['Close']

            elif row['signal'] == -1:  # Sell signal
                cash += shares * row['Close']
                shares = 0

        final_value = cash + (shares * self.data['Close'].iloc[-1])

        return final_value


    def buy_and_hold_pnl(self, initial_cash: float = 1000000) -> float:
        """
        Calculate the final portfolio value using a buy-and-hold strategy.

        Args:
            initial_cash (float): Initial cash available for trading.

        Returns:
            float: Final portfolio value after executing the buy-and-hold strategy.
        """
        
        initial_price = self.data['Close'].iloc[0]
        shares = initial_cash // initial_price
        cash = initial_cash - (shares * initial_price)
        
        final_value = cash + (shares * self.data['Close'].iloc[-1])

        return final_value


    def plot_signals(self) -> tuple:
        '''
        Plot the trading signals on the price chart. Subclasses can call this method and add to the plot.
        
        Returns:
            tuple: Figure and axes objects for the plot.
        '''
        data = self.data

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(data.index, data['Close'], label='Close', linewidth=2, color='black')

        ymin, ymax = ax.get_ylim()
        buy_signals = data[data['signal'] == 1]
        sell_signals = data[data['signal'] == -1]

        ax.vlines(buy_signals.index, ymin, ymax, color='g', alpha=0.2, linestyle='--', label='Buy Signal')
        ax.vlines(sell_signals.index, ymin, ymax, color='r', alpha=0.2, linestyle='--', label='Sell Signal')

        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()

        return fig, ax

