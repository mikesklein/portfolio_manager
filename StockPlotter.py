from fastquant import get_stock_data, backtest
import datetime
import matplotlib.pyplot as plt

class Plotter(object):
    def __init__(self, ticker, period, fast_period, slow_period):
        today = datetime.datetime.now()
        delta = today - datetime.timedelta(days=period)
        self.period = period
        self.slow_period = slow_period
        self.fast_period = fast_period
        self.end_date = today
        self.start_date = delta
        self.tkr = ticker
        self.df = get_stock_data(self.tkr, self.start_date , self.end_date)
        self.MACD()
        self.RSI()
        self.df['SMA_slow'] = self.SMA(period=self.slow_period)
        self.df['SMA_fast'] = self.SMA(period=self.fast_period)
    #simple moving average
    def SMA(self, period=30, column='close'):
        return self.df[column].rolling(window=period).mean()

    #exponential moving average
    def EMA(self, period=20, column='close'):
       return self.df[column].ewm(span=period, adjust=False).mean()

    #calculate the moving average convergence/divergence (MACD)
    #def MACD(data, period_long=26, period_short=12, period_signal=9, column='close'):

    def MACD(self, slow_period=26, fast_period=12, period_signal=9):
        ShortEMA = self.EMA(period=fast_period)
        LongEMA = self.EMA(period=slow_period)
        self.df['MACD'] = ShortEMA - LongEMA
        self.df['Signal'] = self.EMA(period=period_signal, column='MACD')

    def RSI(self, period=14):
        delta = self.df['close'].diff(1)
        delta = delta.dropna()
        up = delta.copy()
        down = delta.copy()
        up[up < 0 ] = 0
        down[down > 0 ] = 0
        self.df['up'] = up
        self.df['down'] = down
        AVG_Gain = self.SMA(period, column='up')
        AVG_Loss = abs(self.SMA(period, column='down'))
        RS = AVG_Gain / AVG_Loss
        RSI = 100.0 - (100.0 / (1.0 + RS))
        self.df['RSI'] = RSI

    def print_df(self):
        print(self.df)

    def plot(self):
        fig, ax = plt.subplots(2,2)
        self.df['close'].plot(ax=ax[0,0], color='black', label='Close Price', title=self.tkr+" Last "+str(self.period)+" Days")
        self.df['SMA_fast'].plot(ax=ax[0,0], color='red', label='SMA ('+str(self.fast_period)+")")
        self.df['SMA_slow'].plot(ax=ax[0,0], color='blue', label='SMA ('+str(self.slow_period)+")")
        self.df['MACD'].plot(ax=ax[1,0], color='blue', label='MACD', title="MACD")
        self.df['Signal'].plot(ax=ax[1,0], color='red', label='Signal')
        self.df['volume'].plot.bar(ax=ax[0,1], color='red', label='Volume', title="Volume")
        self.df['RSI'].plot.bar(ax=ax[1,1], color='red', title="RSI")


        ax[0,0].set_ylabel("Price")
        ax[1,0].set_ylabel("MACD")
        ax[1,1].set_ylabel("RSI")
        ax[0,1].set_ylabel("Volume")

        ax[0, 1].set(xticklabels=[])
        ax[1, 1].set(xticklabels=[])

        ax[0,0].legend()
        ax[1,0].legend()
        ax[1,0].legend()
        ax[1,1].legend()


        plt.tight_layout()
        file_name = self.tkr+".png"
        directory = 'graphs/'
        fig.savefig(directory+file_name)


# plt.show()
# p = Plotter("gdnp.v", 180, 12, 26)
# p.plot()

