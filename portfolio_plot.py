import StockPlotter as plot

stocks = ["gdnp.v", "wfg.to", "ac.to"]
for stock in stocks:
    p = plot.Plotter(stock, 180, 12, 26)
    p.plot()


