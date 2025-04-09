from hyperliquid.info import Info
from hyperliquid.utils import constants
from datetime import datetime, timezone, timedelta
from load_candles import candles_to_df
import numpy as np
import pandas as pd
from trade_data import TradeEngine

hp = {
    "short_size": 10,#3 to 25 step_size=2
    "long_size": 60,#20 to 100 step_size=5
    "volume_enter_scaler": 0.8,#0.5 to 1 step_size=0.1
    "volume_exit_scaler": 1.5,#1 to 3 step_size=0.1
    "trailing_stop_loss": 1.1,#1 to 1.25 step_size=0.02
    "sma_candles": 20,#3 to 10 step_size=1
    "buy_amount": 1000
}
# Initialize the Info class
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Define parameters
# symbols = {"ETH", "BTC", "VINE"}
symbols = {"VINE"}
interval = "15m"
candles = {}

# Set the time range for the candlestick data
# For example, the last 24 hours
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in milliseconds
for symbol in symbols:
    start_time = end_time - (60 * 60 * 1000 * 1265)  # 24 hours ago in milliseconds

    # Fetch candlestick data
    candles[symbol] = info.candles_snapshot(name=symbol, interval=interval, startTime=start_time, endTime=end_time)


df = candles_to_df(candles["VINE"])
print(df.head())

engine = TradeEngine(candles=df, hyperparams=hp)
engine.simulate()


# Output results
print(f"Final Portfolio Value: {engine.PV:.2f}")
print(f"Total Trades: {len(engine.trades)}")
print("Sample Trades:")
for t in engine.trades[-5:]:
    print(t)


trades_df = pd.DataFrame(engine.trades)

# Total stats
num_profitable = (trades_df["pnl"] > 0).sum()
num_losing = (trades_df["pnl"] < 0).sum()

num_volume_exits = (trades_df["exit_reason"] == "volume_sma").sum()
num_trailing_exits = (trades_df["exit_reason"] == "trailing").sum()

print("\n=== Trade Summary ===")
print(f"Total Trades        : {len(trades_df)}")
print(f"Profitable Trades   : {num_profitable}")
print(f"Losing Trades       : {num_losing}")
print(f"Volume-Based Exits  : {num_volume_exits}")
print(f"Trailing SL Exits   : {num_trailing_exits}")